import argparse
import json
import os
import shutil
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple, Iterable


def plan_moves(obj: Dict, pairs: List[Tuple[str, str]], allow_missing: bool) -> Dict:
    planned: Dict[str, object] = {}
    for src, dst in pairs:
        if src in obj:
            planned[dst] = obj[src]
        else:
            if not allow_missing:
                raise KeyError(f"source key not found: {src}")
    return planned


def apply_moves(obj: Dict, planned_writes: Dict[str, object], sources: List[str], on_duplicate: str) -> None:
    for src in sources:
        obj.pop(src, None)

    for dst, value in planned_writes.items():
        if dst in obj:
            if on_duplicate == "error":
                raise KeyError(f"destination key already exists: {dst}")
            elif on_duplicate == "keep_first":
                continue
            elif on_duplicate == "overwrite":
                pass
            else:
                raise ValueError(f"invalid on_duplicate: {on_duplicate}")
        obj[dst] = value


def process_one_file(
    input_path: Path,
    pairs: List[Tuple[str, str]],
    allow_missing: bool,
    on_duplicate: str,
    copy_only: bool,
    make_backup: bool,
) -> Tuple[Path, int]:
    fd, tmp_path = tempfile.mkstemp(suffix=".jsonl", prefix="tmp_", dir=input_path.parent)
    os.close(fd)
    tmp_file = Path(tmp_path)

    pairs_sources = [s for s, _ in pairs]
    line_count = 0

    try:
        with input_path.open("r", encoding="utf-8") as fin, tmp_file.open("w", encoding="utf-8", newline="") as fout:
            for line in fin:
                if not line.strip():
                    continue
                obj = json.loads(line)
                planned = plan_moves(obj, pairs, allow_missing=allow_missing)
                sources = [] if copy_only else pairs_sources
                apply_moves(obj, planned, sources=sources, on_duplicate=on_duplicate)
                json.dump(obj, fout, ensure_ascii=False)
                fout.write("\n")
                line_count += 1

        if make_backup:
            bak = input_path.with_suffix(input_path.suffix + ".bak")
            shutil.copy2(input_path, bak)

        os.replace(tmp_file, input_path)
        return input_path, line_count

    except Exception:
        try:
            if tmp_file.exists():
                tmp_file.unlink()
        finally:
            raise


def iter_target_files(root: Path, pattern: str, recursive: bool) -> Iterable[Path]:
    if recursive:
        yield from root.rglob(pattern)
    else:
        yield from root.glob(pattern)


def main():
    p = argparse.ArgumentParser(description="Multiprocess: move/copy keys across all JSONL files in a directory.")
    p.add_argument("--input-dir", type=Path, required=True, help="Directory containing JSONL files")
    p.add_argument("--pattern", default="*.jsonl", help="Glob pattern (default: *.jsonl)")
    p.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    p.add_argument("--workers", type=int, default=os.cpu_count() or 1, help="Number of processes")
    p.add_argument("--input-keys", nargs="+", required=True, help="Source keys")
    p.add_argument("--output-keys", nargs="+", required=True, help="Destination keys (same length)")
    p.add_argument("--allow-missing", action="store_true", help="Ignore missing source keys")
    p.add_argument(
        "--on-duplicate",
        choices=["error", "keep_first", "overwrite"],
        default="error",
        help="Behavior when destination key already exists",
    )
    p.add_argument("--copy-only", action="store_true", help="Copy (do not delete sources)")
    p.add_argument("--backup", action="store_true", help="Create .bak backup before replace")

    args = p.parse_args()

    if not args.input_dir.is_dir():
        raise NotADirectoryError(f"--input-dir is not a directory: {args.input_dir}")

    if len(args.input_keys) != len(args.output_keys):
        raise ValueError("input-keys and output-keys must have the same length")

    pairs = list(zip(args.input_keys, args.output_keys))
    files = [p for p in iter_target_files(args.input_dir, args.pattern, args.recursive) if p.is_file()]

    if not files:
        print("No files matched.")
        return

    print(f"Found {len(files)} file(s). Start processing with {args.workers} worker(s)...")

    total_lines = 0
    ok = 0
    failed = 0
    errors = []

    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {
            ex.submit(
                process_one_file,
                f,
                pairs,
                args.allow_missing,
                args.on_duplicate,
                args.copy_only,
                args.backup,
            ): f
            for f in files
        }
        for fut in as_completed(futures):
            f = futures[fut]
            try:
                path, n = fut.result()
                ok += 1
                total_lines += n
                print(f"[OK] {path} ({n} lines)")
            except Exception as e:
                failed += 1
                errors.append((f, repr(e)))
                print(f"[ERR] {f}: {e}")

    print(f"\nDone. success={ok}, failed={failed}, total_lines={total_lines}")
    if errors:
        print("Errors:")
        for f, msg in errors:
            print(f" - {f}: {msg}")


if __name__ == "__main__":
    main()
