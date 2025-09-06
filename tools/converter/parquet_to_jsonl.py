import argparse
import json
import sys
from pathlib import Path

from datasets import disable_caching
from datasets import Dataset
import pyarrow as pa
import pyarrow.parquet as pq


def write_jsonl(records_iter, jsonl_file_path: str) -> None:
    with open(jsonl_file_path, "w", encoding="utf-8") as f:
        for rec in records_iter:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")


def convert_with_hf_dataset(parquet_file_path: str, jsonl_file_path: str) -> bool:
    """
    Try converting using Hugging Face Dataset.from_parquet (avoids 'List' features metadata).
    Returns True on success, False to fall back.
    """
    try:
        ds: Dataset = Dataset.from_parquet(parquet_file_path)  # type: ignore
        write_jsonl((row for row in ds), jsonl_file_path)
        return True
    except Exception as e:
        print(f"[INFO] HF Dataset fallback due to: {e.__class__.__name__}: {e}", file=sys.stderr)
        return False


def convert_with_pyarrow(parquet_file_path: str, jsonl_file_path: str, batch_size: int = 65536) -> None:
    """
    Robust fallback using PyArrow streaming. Does not depend on HF features metadata.
    """
    pf = pq.ParquetFile(parquet_file_path)
    with open(jsonl_file_path, "w", encoding="utf-8") as f:
        for batch in pf.iter_batches(batch_size=batch_size):
            # Convert the RecordBatch to a list of Python dicts
            table = pa.Table.from_batches([batch])
            for row in table.to_pylist():
                json.dump(row, f, ensure_ascii=False)
                f.write("\n")


def convert_parquet_to_jsonl(parquet_file_path: str, jsonl_file_path: str) -> None:
    ok = convert_with_hf_dataset(parquet_file_path, jsonl_file_path)
    if not ok:
        convert_with_pyarrow(parquet_file_path, jsonl_file_path)

    print(
        f"Parquet file '{parquet_file_path}' has been converted to JSONL and saved as '{jsonl_file_path}'."
    )


def main() -> None:
    disable_caching()

    parser = argparse.ArgumentParser(description="Convert a Parquet file to JSONL.")
    parser.add_argument("--parquet-file", type=str, required=True, help="Path to the input Parquet file.")
    parser.add_argument("--jsonl-file", type=str, required=True, help="Path to the output JSONL file.")
    args = parser.parse_args()

    in_path = Path(args.parquet_file)
    out_path = Path(args.jsonl_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    convert_parquet_to_jsonl(str(in_path), str(out_path))


if __name__ == "__main__":
    main()
