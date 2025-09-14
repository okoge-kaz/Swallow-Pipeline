import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Dict, Generator

import pyarrow as pa
import pyarrow.ipc as pa_ipc
import pyarrow.feather as feather


def write_jsonl(records_iter: Iterable[Dict], jsonl_file_path: str) -> None:
    with open(jsonl_file_path, "w", encoding="utf-8") as f:
        for rec in records_iter:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")


def _batches_from_ipc_file(path: str) -> Generator[pa.RecordBatch, None, None]:
    with pa.memory_map(path, "r") as source:
        reader = pa_ipc.open_file(source)  # RecordBatchFileReader
        for i in range(reader.num_record_batches):
            yield reader.get_batch(i)


def _batches_from_ipc_stream(path: str) -> Generator[pa.RecordBatch, None, None]:
    with pa.memory_map(path, "r") as source:
        reader = pa_ipc.open_stream(source)  # RecordBatchStreamReader
        for batch in reader:
            yield batch


def _batches_from_feather(
    path: str, batch_size: int
) -> Generator[pa.RecordBatch, None, None]:
    table = feather.read_table(path, memory_map=True)
    for batch in table.to_batches(max_chunksize=batch_size):
        yield batch


def record_batches_from_arrow(
    path: str, batch_size: int
) -> Generator[pa.RecordBatch, None, None]:
    suffix = Path(path).suffix.lower()

    if suffix == ".feather":
        yield from _batches_from_feather(path, batch_size)
        return

    try:
        yield from _batches_from_ipc_file(path)
        return
    except Exception as e_file:
        print(
            f"[INFO] Not IPC file format ({e_file.__class__.__name__}): {e_file}",
            file=sys.stderr,
        )

    try:
        yield from _batches_from_ipc_stream(path)
        return
    except Exception as e_stream:
        print(
            f"[INFO] Not IPC stream format ({e_stream.__class__.__name__}): {e_stream}",
            file=sys.stderr,
        )

    try:
        yield from _batches_from_feather(path, batch_size)
        return
    except Exception as e_feather:
        raise RuntimeError(
            f"Unsupported Arrow file format for '{path}'. "
            f"Tried IPC file, IPC stream, and Feather. Last error: {e_feather.__class__.__name__}: {e_feather}"
        ) from e_feather


def convert_arrow_to_jsonl(
    arrow_file_path: str, jsonl_file_path: str, batch_size: int = 65536
) -> None:
    def rows() -> Generator[Dict, None, None]:
        for batch in record_batches_from_arrow(arrow_file_path, batch_size):
            table = pa.Table.from_batches([batch])
            for row in table.to_pylist():
                yield row

    write_jsonl(rows(), jsonl_file_path)
    print(
        f"Arrow file '{arrow_file_path}' has been converted to JSONL and saved as '{jsonl_file_path}'."
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert an Arrow (IPC/Feather) file to JSONL."
    )
    p.add_argument(
        "--arrow-file",
        type=str,
        required=True,
        help="Path to input .arrow/.ipc/.feather file.",
    )
    p.add_argument(
        "--jsonl-file", type=str, required=True, help="Path to output JSONL file."
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=65536,
        help="Max rows per batch when chunking tables.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    in_path = Path(args.arrow_file)
    out_path = Path(args.jsonl_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    convert_arrow_to_jsonl(str(in_path), str(out_path), batch_size=args.batch_size)


if __name__ == "__main__":
    main()
