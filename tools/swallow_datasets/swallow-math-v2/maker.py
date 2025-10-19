import argparse
import json
import os
import shutil
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, Tuple, List


def iter_target_files(root: Path, pattern: str, recursive: bool) -> Iterable[Path]:
    if recursive:
        yield from root.rglob(pattern)
    else:
        yield from root.glob(pattern)


def transform_value(val: str, marker: str) -> Tuple[bool, str]:
    idx = val.rfind(marker)
    if idx == -1:
        return False, val
    after = val[idx + len(marker) :]
    after = after.lstrip()
    if after != val:
        return True, after
    return False, val


def process_one_file(
    input_path: Path,
    input_key: str,
    marker: str,
    make_backup: bool,
) -> Tuple[Path, int, int]:
    fd, tmp_path = tempfile.mkstemp(suffix=".jsonl", prefix="tmp_", dir=input_path.parent)
    os.close(fd)
    tmp_file = Path(tmp_path)

    total = 0
    changed = 0

    try:
        with input_path.open("r", encoding="utf-8") as fin, tmp_file.open("w", encoding="utf-8", newline="") as fout:
            for line in fin:
                if not line.strip():
                    continue
                total += 1
                obj = json.loads(line)

                val = obj.get(input_key, None)
                if isinstance(val, str):
                    did_change, new_val = transform_value(val, marker)
                    if did_change:
                        obj[input_key] = new_val
                        changed += 1

                json.dump(obj, fout, ensure_ascii=False)
                fout.write("\n")

        if make_backup:
            bak = input_path.with_suffix(input_path.suffix + ".bak")
            shutil.copy2(input_path, bak)

        os.replace(tmp_file, input_path)
        return input_path, total, changed

    except Exception:
        try:
            if tmp_file.exists():
                tmp_file.unlink()
        finally:
            raise


def main():
    ap = argparse.ArgumentParser(
        description="Multiprocess in-place JSONL edit: keep text after the last marker for a given input key."
    )
    ap.add_argument("--input-dir", type=Path, required=True, help="JSONL を含むディレクトリ")
    ap.add_argument("--pattern", default="*.jsonl", help="グロブパターン (既定: *.jsonl)")
    ap.add_argument("--recursive", action="store_true", help="サブディレクトリも再帰的に処理")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1, help="並列プロセス数")
    ap.add_argument("--input-key", required=True, help="対象のキー名（文字列値を想定）")
    ap.add_argument(
        "--marker", "--maker", dest="marker", default="<|MATH_TEXT|>", help="分割マーカー（既定: <|MATH_TEXT|>）"
    )
    ap.add_argument("--backup", action="store_true", help="置換前に <file>.jsonl.bak を作成")

    args = ap.parse_args()

    if not args.input_dir.is_dir():
        raise NotADirectoryError(f"--input-dir がディレクトリではありません: {args.input_dir}")

    files: List[Path] = [p for p in iter_target_files(args.input_dir, args.pattern, args.recursive) if p.is_file()]
    if not files:
        print("対象ファイルが見つかりませんでした。")
        return

    print(f"Found {len(files)} file(s). Start processing with {args.workers} worker(s)...")

    total_files = 0
    total_records = 0
    total_changed = 0
    failed = 0

    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(process_one_file, f, args.input_key, args.marker, args.backup): f for f in files}
        for fut in as_completed(futures):
            f = futures[fut]
            try:
                path, n_total, n_changed = fut.result()
                total_files += 1
                total_records += n_total
                total_changed += n_changed
                print(f"[OK] {path}  records={n_total}  changed={n_changed}")
            except Exception as e:
                failed += 1
                print(f"[ERR] {f}: {e}")

    print("\n=== Summary ===")
    print(f"processed files : {total_files}")
    print(f"failed files    : {failed}")
    print(f"total records   : {total_records}")
    print(f"changed records : {total_changed}")


if __name__ == "__main__":
    main()
