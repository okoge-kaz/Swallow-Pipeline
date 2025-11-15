#!/usr/bin/env python3
import argparse
import json
import random
import re
from pathlib import Path
from typing import List

# Regex for detecting Chinese characters (CJK Unified Ideographs + Extensions, without kana)
CHINESE_REGEX = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")


def extract_chinese_chars(text: str) -> str:
    """Return only the Chinese characters in the given text."""
    return "".join(CHINESE_REGEX.findall(text))


def process_files(input_paths: List[Path], output_path: Path, verbose: bool) -> None:
    data = []
    skipped = 0

    for input_path in input_paths:
        with open(input_path, "r", encoding="utf-8") as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as e:
                    if verbose:
                        print(f"[WARN] Skipping invalid JSON at {input_path}:{line_num}: {e}")
                    continue

                messages = item.get("messages", [])
                if not isinstance(messages, list):
                    continue

                chinese_hits = []
                for msg in messages:
                    if not isinstance(msg, dict):
                        continue
                    content = msg.get("content", "")
                    if not isinstance(content, str):
                        continue
                    chars = extract_chinese_chars(content)
                    if chars:
                        chinese_hits.append(chars)

                if chinese_hits:
                    skipped += 1
                    if verbose:
                        for chars in chinese_hits:
                            print(f"[SKIP] {input_path}:{line_num} -> {chars}")
                    continue

                data.append(item)

    # shuffle valid data
    random.shuffle(data)

    # write output
    with open(output_path, "w", encoding="utf-8") as outfile:
        for item in data:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write("\n")

    print(f"[INFO] Processed {len(input_paths)} files")
    print(f"[INFO] Saved {len(data)} items to {output_path}")
    print(f"[INFO] Skipped {skipped} items containing Chinese")


def main():
    parser = argparse.ArgumentParser(description="Filter out JSONL entries containing Chinese text")
    parser.add_argument(
        "--input-jsonls",
        type=str,
        nargs="+",
        required=True,
        help="Input JSONL file paths",
    )
    parser.add_argument("--output-jsonl", type=str, required=True, help="Output JSONL file path")
    parser.add_argument("--verbose", action="store_true", help="Show skipped Chinese characters only")
    args = parser.parse_args()

    input_paths = [Path(p) for p in args.input_jsonls]
    output_path = Path(args.output_jsonl)

    process_files(input_paths, output_path, args.verbose)


if __name__ == "__main__":
    main()
