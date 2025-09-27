import argparse
import json
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description="Deduplicate JSONL by conversation[0][content]")
    parser.add_argument("--input-jsonl", type=str, required=True, help="Input JSONL file")
    parser.add_argument("--output-jsonl", type=str, required=True, help="Output JSONL file")
    args = parser.parse_args()

    seen = set()
    unique_items = []

    with open(args.input_jsonl, "r", encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)

    with open(args.input_jsonl, "r", encoding="utf-8") as infile:
        for line in tqdm(infile, total=total_lines, desc="Deduplicating"):
            if not line.strip():
                continue
            item = json.loads(line)

            try:
                key = item["conversation"][0]["content"]
            except (KeyError, IndexError, TypeError):
                continue

            if key not in seen:
                seen.add(key)
                unique_items.append(item)

    with open(args.output_jsonl, "w", encoding="utf-8") as outfile:
        for item in unique_items:
            outfile.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\nProcessed {len(unique_items)} unique items written to {args.output_jsonl}")


if __name__ == "__main__":
    main()
