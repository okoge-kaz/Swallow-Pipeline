import argparse
import json
import random


def main():
    parser = argparse.ArgumentParser(description="Filter and sample JSONL by num_token")
    parser.add_argument("--input-jsonl", type=str, required=True, help="Input JSONL file")
    parser.add_argument("--output-jsonl", type=str, required=True, help="Output JSONL file")
    parser.add_argument("--max-tokens", type=int, required=True, help="Maximum allowed num_token")
    parser.add_argument(
        "--num-samples", type=int, default=None, help="Number of random samples to select (after filtering)"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    random.seed(args.seed)

    filtered_data = []
    with open(args.input_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("num_token", 0) <= args.max_tokens:
                filtered_data.append(obj)

    if args.num_samples is not None and args.num_samples < len(filtered_data):
        filtered_data = random.sample(filtered_data, args.num_samples)

    with open(args.output_jsonl, "w", encoding="utf-8") as out_f:
        for obj in filtered_data:
            out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(f"Filtered {len(filtered_data)} samples written to {args.output_jsonl}")


if __name__ == "__main__":
    main()
