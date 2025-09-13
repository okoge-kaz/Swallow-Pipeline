import argparse
import json
import random
from typing import cast
from pathlib import Path


def process_file(input_path: Path, output_path: Path, with_system_prompt: bool) -> None:
    with open(input_path, "r", encoding="utf-8") as infile:
        data = [json.loads(line) for line in infile if line.strip()]

    random.shuffle(data)
    system_message = {"role": "system", "content": "あなたは誠実で優秀な日本人のアシスタントです"}
    write_data = []

    for item in data:
        if "conversation" in item and isinstance(item["conversation"], list):
            item["conversation"] = cast(list, item["conversation"])

            if with_system_prompt:
                item["conversation"] = [system_message] + item["conversation"]

            if any(len(msg["content"]) <= 0 for msg in item["conversation"]):
                print(f"[LOG] Skipping item with empty content")
                continue

            write_data.append(item)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for item in write_data:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Shuffle JSONL and optionally prepend system message.")
    parser.add_argument("--input-jsonl", type=Path, required=True, help="Path to input JSONL file")
    parser.add_argument("--output-jsonl", type=Path, required=True, help="Path to output JSONL file")
    parser.add_argument(
        "--with-system-prompt",
        action="store_true",
        help="If set, prepend system message to each conversation",
    )
    args = parser.parse_args()

    process_file(args.input_jsonl, args.output_jsonl, args.with_system_prompt)


if __name__ == "__main__":
    main()
