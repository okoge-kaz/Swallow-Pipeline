#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read all parquet under --input-dir, take (repo, commit_id, rel_path),
group by major language (mapped from rel_path's extension), and write to:
  --output-dir/<lang>/train_0000001.parquet

- Only major languages (predefined mapping) are kept; others are ignored.
- Works with PyArrow 21.0.0
"""

import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple, List

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


# 拡張子 → 出力ディレクトリ名（主要言語のみ）
EXT_TO_LANG: Dict[str, str] = {
    # systems
    "c": "c",
    "h": "headers", "hpp": "headers", "hh": "headers", "hxx": "headers",
    "cpp": "cpp", "cc": "cpp", "cxx": "cpp",
    "cu": "cuda", "cuh": "cuda",
    # general
    "py": "python",
    "java": "java",
    "go": "go",
    "rs": "rust",
    "rb": "ruby",
    "php": "php",
    "cs": "csharp",
    "swift": "swift",
    "kt": "kotlin",
    "m": "objectivec", "mm": "objectivec",
    # web
    "js": "javascript", "jsx": "javascript",
    "ts": "typescript", "tsx": "typescript",
    "html": "html", "htm": "html",
    "css": "css",
    # configs / data (必要なら保持)
    "json": "json",
    "yml": "yaml", "yaml": "yaml",
    "toml": "toml", "ini": "ini",
    # docs
    "md": "markdown",
    # db
    "sql": "sql",
    # shells
    "sh": "shell", "bash": "shell", "zsh": "shell",
}

# 許容する言語ディレクトリ（上の値の集合）
ALLOWED_LANGS = set(EXT_TO_LANG.values())


def parse_args():
    p = argparse.ArgumentParser(description="Split parquet rows by major language and shard to train_*.parquet")
    p.add_argument("--input-dir", required=True, help="Directory containing parquet files (recursively scanned)")
    p.add_argument("--output-dir", required=True, help="Output root directory")
    p.add_argument("--rows-per-file", type=int, default=200_000, help="Max rows per output parquet (default: 200k)")
    p.add_argument("--batch-size", type=int, default=100_000, help="Dataset Scanner batch size (default: 100k)")
    p.add_argument("--compression", type=str, default="snappy", help="Parquet codec: snappy|zstd|gzip|none")
    return p.parse_args()


def ext_to_lang(rel_path: Optional[str]) -> Optional[str]:
    """rel_path から拡張子を取り、主要言語にマップ。非対応は None（無視）。"""
    if not rel_path:
        return None
    s = rel_path.strip().rstrip(".")
    if "." not in s:
        return None
    ext = s.rsplit(".", 1)[-1].lower()
    lang = EXT_TO_LANG.get(ext)
    if lang in ALLOWED_LANGS:
        return lang
    return None  # 非主要言語は無視


class RotatingParquetWriter:
    """言語ごとに ParquetWriter を管理し、rows-per-file 毎にローテーション。"""
    def __init__(self, out_root: Path, rows_per_file: int, compression: str):
        self.out_root = out_root
        self.rows_per_file = rows_per_file
        self.compression = None if compression.lower() == "none" else compression
        self._writers: Dict[str, Tuple[pq.ParquetWriter, int, int, pa.Schema]] = {}

    def _next_path(self, lang: str, index: int) -> Path:
        d = self.out_root / lang
        d.mkdir(parents=True, exist_ok=True)
        return d / f"train_{index:07d}.parquet"

    def _open_new(self, lang: str, schema: pa.Schema):
        _, _, idx, _ = self._writers.get(lang, (None, 0, 0, schema))
        idx += 1
        path = self._next_path(lang, idx)
        w = pq.ParquetWriter(path, schema=schema, compression=self.compression)
        self._writers[lang] = (w, 0, idx, schema)
        print(f"[{lang}] open  {path}")

    def write(self, lang: str, table: pa.Table):
        if table.num_rows == 0:
            return
        if lang not in self._writers:
            self._open_new(lang, table.schema)
        w, cur, idx, schema = self._writers[lang]
        if table.schema != schema:
            table = table.cast(schema)
        off = 0
        total = table.num_rows
        while off < total:
            cap = self.rows_per_file - cur
            if cap <= 0:
                w.close()
                print(f"[{lang}] close (rows={cur})")
                self._open_new(lang, schema)
                w, cur, idx, schema = self._writers[lang]
                cap = self.rows_per_file
            take = min(cap, total - off)
            shard = table.slice(off, take)
            w.write_table(shard)
            cur += take
            off += take
            self._writers[lang] = (w, cur, idx, schema)

    def close_all(self):
        for lang, (w, cur, idx, _) in list(self._writers.items()):
            w.close()
            print(f"[{lang}] close (rows={cur})")


def main():
    args = parse_args()
    in_root = Path(args.input_dir)
    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    dataset = ds.dataset(str(in_root), format="parquet")
    required = ["repo", "commit_id", "rel_path"]
    for c in required:
        if c not in dataset.schema.names:
            raise ValueError(f"Missing column '{c}'. Schema: {dataset.schema}")

    scanner = ds.Scanner.from_dataset(dataset, columns=required, batch_size=args.batch_size)
    writer = RotatingParquetWriter(out_root, args.rows_per_file, args.compression)

    processed = 0
    kept = 0
    skipped = 0

    for rb in scanner.to_batches():
        tbl = pa.Table.from_batches([rb])
        repos: List[str] = tbl.column("repo").to_pylist()
        commits: List[str] = tbl.column("commit_id").to_pylist()
        rels: List[str] = tbl.column("rel_path").to_pylist()

        # 言語ごとにグルーピング（非主要言語は捨てる）
        grouped: Dict[str, list] = {}
        for r, c, p in zip(repos, commits, rels):
            lang = ext_to_lang(p)
            if lang is None:
                skipped += 1
                continue
            grouped.setdefault(lang, []).append((r, c, p))
            kept += 1

        # Arrow Table に変換して書き込み
        for lang, rows in grouped.items():
            col_repo, col_commit, col_rel = zip(*rows)
            part = pa.table({
                "repo": pa.array(col_repo, type=pa.string()),
                "commit_id": pa.array(col_commit, type=pa.string()),
                "rel_path": pa.array(col_rel, type=pa.string()),
            })
            writer.write(lang, part)

        processed += tbl.num_rows
        if processed % (args.batch_size * 10) == 0:
            print(f"... processed={processed}, kept={kept}, skipped={skipped}")

    writer.close_all()
    print(f"Done. processed={processed}, kept={kept}, skipped={skipped}")


if __name__ == "__main__":
    main()
