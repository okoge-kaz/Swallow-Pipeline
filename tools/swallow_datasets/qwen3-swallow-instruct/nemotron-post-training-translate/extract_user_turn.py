import argparse
import json

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract user turns from conversations in JSONL files."
    )
    parser.add_argument(
        "--input-jsonl",
        type=str,
        required=True,
        help="Path to the input JSONL file.",
    )
    parser.add_argument(
        "--output-jsonl",
        type=str,
        required=True,
        help="Path to the output JSONL file.",
    )
    return parser.parse_args()

def extract_user_turns(input_jsonl: str, output_jsonl: str) -> None:
    with open(input_jsonl, "r", encoding="utf-8") as infile, open(output_jsonl, "w", encoding="utf-8") as outfile:
        for line in infile:
            record = json.loads(line)
            conversation = record.get("conversation", [])
            record["english_conversation"] = conversation
            del record["conversation"]
            del record["text_qwen3"]
            del record["text_gpt_oss"]
            del record["output"]

            outfile.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    extract_user_turns(args.input_jsonl, args.output_jsonl)

if __name__ == "__main__":
    main()
