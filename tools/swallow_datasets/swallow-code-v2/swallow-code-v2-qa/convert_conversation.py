#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def process_file(input_path: Path, output_path: Path) -> None:
    """1つの jsonl ファイルを変換して output_path に書き出す。"""
    with input_path.open("r", encoding="utf-8") as f_in, output_path.open("w", encoding="utf-8") as f_out:
        for lineno, line in enumerate(f_in, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                print(
                    f"[WARN] {input_path}:{lineno} で JSON デコードに失敗しました: {e}",
                    file=sys.stderr,
                )
                continue

            if "question" not in item:
                print(
                    f"[WARN] {input_path}:{lineno} に 'question' キーがありません。スキップします。",
                    file=sys.stderr,
                )
                continue

            question_text = item["question"]

            new_item = {
                "conversation": [
                    {
                        "role": "user",
                        "content": question_text,
                    }
                ]
            }

            f_out.write(json.dumps(new_item, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Convert jsonl lines with 'question' key into conversation format.")
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="入力 jsonl ファイルが置かれたディレクトリ",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="出力先ディレクトリ。指定しない場合は元ファイルを上書きします。",
    )
    args = parser.parse_args(argv)

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"[ERROR] --input-dir {input_dir} はディレクトリではありません。", file=sys.stderr)
        sys.exit(1)

    output_dir: Optional[Path] = None
    if args.output_dir is not None:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_files = sorted(input_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"[WARN] {input_dir} に *.jsonl ファイルが見つかりません。", file=sys.stderr)

    for in_path in jsonl_files:
        if output_dir is not None:
            out_path = output_dir / in_path.name
            print(f"[INFO] {in_path} -> {out_path}")
            process_file(in_path, out_path)
        else:
            # in-place 書き換え: 一旦 tmp に書いてから rename
            tmp_path = in_path.with_suffix(in_path.suffix + ".tmp")
            print(f"[INFO] {in_path} を上書き変換します。", file=sys.stderr)
            process_file(in_path, tmp_path)
            tmp_path.replace(in_path)


if __name__ == "__main__":
    main()
