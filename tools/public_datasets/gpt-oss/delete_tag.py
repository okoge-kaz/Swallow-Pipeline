import argparse
import json
import gzip
from pathlib import Path
from typing import IO, Dict, Any, Iterable


def _open_maybe_gzip(path: Path, mode: str) -> IO[str]:
    if str(path).endswith(".gz"):
        return gzip.open(path, mode + "t", encoding="utf-8", newline="\n")
    return open(path, mode, encoding="utf-8", newline="\n")


def iter_jsonl(fp: IO[str]) -> Iterable[Dict[str, Any]]:
    for i, line in enumerate(fp, 1):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except Exception as e:
            raise ValueError(f"Invalid JSON at line {i}: {e}")


def contains_special_token(obj: Any) -> bool:
    """再帰的に走査して特殊トークンが含まれているか判定"""
    special_tokens = ["<|end|>", "<|start|>", "<|channel|>", "<|message|>"]
    if isinstance(obj, str):
        return any(tok in obj for tok in special_tokens)
    elif isinstance(obj, dict):
        return any(contains_special_token(v) for v in obj.values())
    elif isinstance(obj, list):
        return any(contains_special_token(v) for v in obj)
    return False


def main():
    ap = argparse.ArgumentParser(
        description="Detect and optionally filter records containing <|end|>, <|start|>, <|channel|>, or <|message|>."
    )
    ap.add_argument("--input-jsonl", required=True, type=Path)
    ap.add_argument("--output-jsonl", type=Path, help="Path to save filtered records")
    ap.add_argument("--remove", action="store_true", help="Remove those containing special tokens")
    args = ap.parse_args()

    total = 0
    bad = 0
    filtered_records = []

    with _open_maybe_gzip(args.input_jsonl, "r") as fp:
        for rec in iter_jsonl(fp):
            total += 1
            if contains_special_token(rec):
                bad += 1
                if not args.remove:
                    continue
            else:
                filtered_records.append(rec)

    print(f"Total records: {total}")
    print(f"Records containing <|end|>, <|start|>, <|channel|>, or <|message|>: {bad}")
    print(f"Clean records (without those tokens): {total - bad}")

    if args.remove:
        if not args.output_jsonl:
            raise ValueError("--output-jsonl must be specified when using --remove")
        with _open_maybe_gzip(args.output_jsonl, "w") as out_fp:
            for rec in filtered_records:
                out_fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"Filtered file saved to: {args.output_jsonl}")


if __name__ == "__main__":
    main()
