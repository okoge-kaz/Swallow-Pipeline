#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import gzip
import json
import os
import shutil
import sys
import tempfile
from functools import partial
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Iterable, Optional, Tuple, List


def is_jsonl(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".jsonl") or name.endswith(".jsonl.gz")


def iter_lines(path: Path) -> Iterable[str]:
    if path.suffix.lower() == ".gz" or path.name.lower().endswith(".jsonl.gz"):
        with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
            for line in f:
                yield line
    else:
        with path.open("r", encoding="utf-8", newline="") as f:
            for line in f:
                yield line


def open_writer_atomic(dest_path: Path):
    """同一ディレクトリにテンポラリを作って返す"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, dir=str(dest_path.parent)) as tmp:
        tmp_name = tmp.name
    os.unlink(tmp_name)
    if dest_path.suffix.lower() == ".gz" or dest_path.name.lower().endswith(".jsonl.gz"):
        f = gzip.open(tmp_name, "wt", encoding="utf-8", newline="")
    else:
        f = open(tmp_name, "w", encoding="utf-8", newline="")
    return f, tmp_name


def process_record(line: str, target_key: str, drop_missing: bool) -> Optional[str]:
    line = line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None

    # "text" と target_key を削除（上書き前提）
    obj.pop("text", None)
    value = obj.pop(target_key, None)  # 元の key も削除

    # 値が存在すれば text にコピー
    if value is not None:
        obj["text"] = value
    else:
        if drop_missing:
            return None

    return json.dumps(obj, ensure_ascii=False)


def process_one_file(
    idx_total_in_out: Tuple[int, int, Path],
    target_key: str,
    drop_missing: bool,
    report_every: int,
) -> Tuple[str, int, int, int]:
    idx, total_files, in_path = idx_total_in_out
    kept = 0
    dropped = 0
    seen = 0

    writer, tmp_name = open_writer_atomic(in_path)
    try:
        with writer as fout:
            for line in iter_lines(in_path):
                seen += 1
                rec = process_record(line, target_key=target_key, drop_missing=drop_missing)
                if rec is None:
                    dropped += 1
                else:
                    kept += 1
                    fout.write(rec + "\n")

                if report_every > 0 and (seen % report_every) == 0:
                    print(
                        f"[{idx}/{total_files}] {in_path.name}: {seen:,} lines processed...",
                        file=sys.stdout,
                        flush=True,
                    )

        shutil.move(tmp_name, in_path)
    except Exception as e:
        try:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)
        except Exception:
            pass
        raise e

    print(
        f"[DONE {idx}/{total_files}] {in_path.name}  kept={kept:,}  dropped={dropped:,}  lines={seen:,}",
        flush=True,
    )
    return (str(in_path), kept, dropped, seen)


def collect_targets(input_dir: Path) -> List[Path]:
    return [p for p in sorted(input_dir.rglob("*")) if p.is_file() and is_jsonl(p)]


def main():
    ap = argparse.ArgumentParser(
        description="In-place rewrite JSONL(.gz): copy --target-key into 'text', remove original key and existing 'text'."
    )
    ap.add_argument("--input-dir", type=Path, required=True, help="入力ディレクトリ（再帰探索）")
    ap.add_argument("--target-key", type=str, required=True, help="このキーの値を 'text' にコピー（元キーは削除）")
    ap.add_argument("--drop-missing", action="store_true", help="--target-key が無いレコードは出力から除外")
    ap.add_argument("--workers", type=int, default=max(1, cpu_count() // 2), help="並列ワーカー数")
    ap.add_argument("--report-every", type=int, default=20000, help="進捗表示行間隔（0で無効）")
    args = ap.parse_args()

    files = collect_targets(args.input_dir)
    if not files:
        print(f"[INFO] No JSONL files found under: {args.input_dir}")
        return

    total = len(files)
    print(f"[INFO] Target files: {total}  | workers={args.workers}")
    for i, f in enumerate(files, start=1):
        print(f"  - [{i}/{total}] {f}", flush=True)

    kept_total = dropped_total = seen_total = 0
    job_args = [(i, total, f) for i, f in enumerate(files, start=1)]
    fn = partial(
        process_one_file,
        target_key=args.target_key,
        drop_missing=args.drop_missing,
        report_every=args.report_every,
    )

    if args.workers <= 1:
        for triple in job_args:
            _, kept, dropped, seen = fn(triple)
            kept_total += kept
            dropped_total += dropped
            seen_total += seen
    else:
        with Pool(processes=args.workers) as pool:
            for _, kept, dropped, seen in pool.imap_unordered(fn, job_args, chunksize=1):
                kept_total += kept
                dropped_total += dropped
                seen_total += seen

    print(
        f"[SUMMARY] files={total:,}  lines={seen_total:,}  kept={kept_total:,}  dropped={dropped_total:,}",
        flush=True,
    )


if __name__ == "__main__":
    main()
