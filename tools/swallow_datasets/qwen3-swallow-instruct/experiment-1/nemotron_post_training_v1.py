import argparse
import json
from pathlib import Path


def process_file(input_path: Path, output_path: Path, dataset_name: str, former_key: str, new_key: str) -> None:
    with open(input_path, "r", encoding="utf-8") as infile:
        data = [json.loads(line) for line in infile if line.strip()]

    write_data = []
    for item in data:
        if former_key not in item:
            continue

        item[new_key] = item[former_key]
        item["dataset_name"] = dataset_name

        del item[former_key]
        write_data.append(item)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for item in write_data:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--dataset-name", type=str, required=True)
    parser.add_argument("--former-jsonl-key", type=str, required=True, help="The key to replace (e.g., messages)")
    parser.add_argument("--new-jsonl-key", type=str, required=True, help="The new key name (e.g., conversation)")
    args = parser.parse_args()

    process_file(args.input_jsonl, args.output_jsonl, args.dataset_name, args.former_jsonl_key, args.new_jsonl_key)


if __name__ == "__main__":
    main()
