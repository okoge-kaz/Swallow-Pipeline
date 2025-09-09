import argparse
import gzip
import json
import os
import re
import sys
import tempfile
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Iterable, Optional, Tuple, List, Dict

THINK_PATTERN = re.compile(r"<think>.*?</think>", flags=re.DOTALL)

MATH_SOURCES = {s.lower() for s in ["OpenMathReasoning", "NuminaMath-CoT"]}
CODE_SOURCES = {s.lower() for s in ["OpenCodeReasoning", "MagicoderEvolInstruct", "opc-sft-stage2", "leetcode", "TACO", "apps"]}

def open_maybe_gzip(path: Path, mode: str):
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8", newline="")
    return open(path, mode, encoding="utf-8", newline="")

def clean_think(text: str) -> str:
    """Remove <think>...</think> and any leading newlines after removal."""
    if not text:
        return text
    cleaned = THINK_PATTERN.sub("", text)
    cleaned = re.sub(r'^(?:\r?\n)+', '', cleaned)
    return cleaned

def iter_jsonl_records(path: Path) -> Iterable[Tuple[int, dict]]:
    with open_maybe_gzip(path, "rt") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] {path}: line {i}: JSON decode error: {e}", file=sys.stderr)
                continue
            yield i, obj

def build_output_item(data: dict, keep_think: bool) -> Optional[dict]:
    if "input" not in data or "output" not in data:
        return None
    inp = data.get("input", "")
    out = data.get("output", "")
    if not keep_think:
        out = clean_think(out)
    return {
        "text": f"Question:\n\n{inp}\n\nSolution:\n\n{out}",
        "conversation": [
            {"role": "user", "content": inp},
            {"role": "assistant", "content": out},
        ],
    }

def extract_source(data: dict) -> Optional[str]:
    """
    Try to extract a canonical source string from data["source"].
    Accepts str or list; returns lowercased string if matched.
    """
    src = data.get("source")
    if src is None:
        return None
    candidates: List[str] = []
    if isinstance(src, str):
        candidates = [src]
    elif isinstance(src, list):
        candidates = [str(s) for s in src if isinstance(s, (str, int, float))]
    else:
        try:
            candidates = [str(src)]
        except Exception:
            candidates = []
    # normalize and try to find an exact known match by token or substring
    lcands = [c.strip().lower() for c in candidates if c]
    for c in lcands:
        # exact match to known labels
        if c in MATH_SOURCES or c in CODE_SOURCES:
            return c
        # substring fallback (handles variants like "openmathreasoning-v1")
        for known in MATH_SOURCES | CODE_SOURCES:
            if known in c:
                return known
    return None

def categorize_source(src_lc: Optional[str]) -> Optional[str]:
    if src_lc is None:
        return None
    if src_lc in MATH_SOURCES:
        return "math"
    if src_lc in CODE_SOURCES:
        return "code"
    return None

def process_one_file(args) -> Tuple[Path, Path, Dict[str, int]]:
    """
    Process a single input file into two temp JSONL files (math/code).
    Returns (math_tmp_path, code_tmp_path, stats)
    """
    in_path, keep_think, tmp_dir = args
    safe = in_path.name.replace(os.sep, "_")
    math_tmp = Path(tmp_dir) / f"{safe}.math.tmp.jsonl"
    code_tmp = Path(tmp_dir) / f"{safe}.code.tmp.jsonl"

    written_math = written_code = skipped = unknown = 0

    # open lazily to avoid empty files? We'll create them anyway so merging is simpler.
    f_math = open(math_tmp, "w", encoding="utf-8", newline="")
    f_code = open(code_tmp, "w", encoding="utf-8", newline="")

    try:
        for line_no, obj in iter_jsonl_records(in_path):
            cat = categorize_source(extract_source(obj))
            if cat is None:
                unknown += 1
                continue
            item = build_output_item(obj, keep_think=keep_think)
            if item is None:
                skipped += 1
                print(f"[WARN] {in_path}: line {line_no}: missing 'input' or 'output', skipped.", file=sys.stderr)
                continue
            if cat == "math":
                f_math.write(json.dumps(item, ensure_ascii=False) + "\n")
                written_math += 1
            elif cat == "code":
                f_code.write(json.dumps(item, ensure_ascii=False) + "\n")
                written_code += 1
    finally:
        f_math.close()
        f_code.close()

    stats = {
        "written_math": written_math,
        "written_code": written_code,
        "skipped": skipped,
        "unknown_source": unknown,
    }
    return math_tmp, code_tmp, stats

def discover_input_files(input_dir: Path, recursive: bool) -> List[Path]:
    if recursive:
        return sorted(list(input_dir.rglob("*.jsonl")) + list(input_dir.rglob("*.jsonl.gz")))
    return sorted(list(input_dir.glob("*.jsonl")) + list(input_dir.glob("*.jsonl.gz")))

def merge_files(temp_files: List[Path], output_path: Path) -> int:
    count = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as out_f:
        for p in temp_files:
            if not p.exists():
                continue
            with open(p, "r", encoding="utf-8") as in_f:
                for line in in_f:
                    out_f.write(line)
                    count += 1
    return count

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build JSONL (text + conversation) from inputs, categorized by source into math/code."
    )
    parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing *.jsonl or *.jsonl.gz")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory to write train_math.jsonl / train_code.jsonl")
    parser.add_argument("--num-proc", type=int, default=max(1, cpu_count() // 2), help="Worker processes")
    parser.add_argument("--with-think-trajectory", action="store_true", help="Keep <think>…</think> content if set")
    parser.add_argument("--recursive", action="store_true", help="Recursively search input files")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir
    keep_think: bool = args.with_think_trajectory
    num_proc: int = max(1, args.num_proc)

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[ERROR] --input-dir not found or not a directory: {input_dir}", file=sys.stderr)
        sys.exit(1)

    files = discover_input_files(input_dir, args.recursive)
    if not files:
        print(f"[WARN] No input files found under: {input_dir}", file=sys.stderr)
        # still create empty outputs
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "train_math.jsonl").write_text("", encoding="utf-8")
        (output_dir / "train_code.jsonl").write_text("", encoding="utf-8")
        return

    print(f"[INFO] Found {len(files)} files.", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="catjsonl_") as tmp_dir:
        tasks = [(p, keep_think, tmp_dir) for p in files]
        results = []
        try:
            with Pool(processes=num_proc) as pool:
                for res in pool.imap_unordered(process_one_file, tasks):
                    results.append(res)
                    mtmp, ctmp, stats = res
                    print(
                        f"[INFO] {Path(mtmp).name.replace('.math.tmp.jsonl','')}: "
                        f"math={stats['written_math']}, code={stats['written_code']}, "
                        f"skipped={stats['skipped']}, unknown_source={stats['unknown_source']}",
                        file=sys.stderr,
                    )
        except KeyboardInterrupt:
            print("[ERROR] Interrupted by user.", file=sys.stderr)
            sys.exit(130)

        # preserve deterministic merge order following sorted input files
        math_map = {Path(r[0]).name.replace(".math.tmp.jsonl",""): Path(r[0]) for r in results}
        code_map = {Path(r[1]).name.replace(".code.tmp.jsonl",""): Path(r[1]) for r in results}

        ordered_math_tmps = [math_map.get(f.name, None) for f in files]
        ordered_code_tmps = [code_map.get(f.name, None) for f in files]
        ordered_math_tmps = [p for p in ordered_math_tmps if isinstance(p, Path)]
        ordered_code_tmps = [p for p in ordered_code_tmps if isinstance(p, Path)]

        out_math = output_dir / "train_math.jsonl"
        out_code = output_dir / "train_code.jsonl"

        total_math = merge_files(ordered_math_tmps, out_math)
        total_code = merge_files(ordered_code_tmps, out_code)

        print(f"[INFO] Wrote {out_math} (lines={total_math})", file=sys.stderr)
        print(f"[INFO] Wrote {out_code} (lines={total_code})", file=sys.stderr)

if __name__ == "__main__":
    main()
