import argparse
import json
import re
import random
from tqdm import tqdm


def is_valid_item(item):
    # Check if "conversation" exists and has at least 2 turns
    if "conversation" not in item or len(item["conversation"]) < 2:
        print("⚠️ Removing item: 'conversation' missing or has fewer than 2 turns")
        return False

    conv = item["conversation"]

    # Each turn must have non-empty content (ignoring whitespace/newlines)
    for idx, turn in enumerate(conv):
        content = turn.get("content", "")
        role = turn.get("role", "")
        if role == "system":
            continue  # Skip system role checks

        if len(re.sub(r"[\s\n]", "", content)) < 1:
            print(f"⚠️ Removing item: empty content at index={idx}")
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Filter and shuffle JSONL conversations")
    parser.add_argument("--input-jsonl", type=str, required=True, help="Path to input JSONL file")
    parser.add_argument("--output-jsonl", type=str, required=True, help="Path to output JSONL file")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling")
    args = parser.parse_args()

    valid_items = []
    with open(args.input_jsonl, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Checking JSONL"):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                print("⚠️ Removing item: invalid JSON format")
                continue

            if is_valid_item(item):
                valid_items.append(item)

    # Shuffle valid items
    random.seed(args.seed)
    random.shuffle(valid_items)

    # Write shuffled items to output JSONL
    with open(args.output_jsonl, "w", encoding="utf-8") as f:
        for item in valid_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Done: {len(valid_items)} valid items saved after filtering and shuffling")


if __name__ == "__main__":
    main()
