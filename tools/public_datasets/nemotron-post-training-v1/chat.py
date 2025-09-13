import argparse
import json
from pathlib import Path
from tqdm import tqdm


def load_jsonl(path: Path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def main():
    parser = argparse.ArgumentParser(description="Fill missing user content from lmsys-chat-1m dataset")
    parser.add_argument("--input-jsonl", type=Path, required=True, help="Input JSONL file with uuid and messages")
    parser.add_argument("--lmsys-chat-1m-paths", type=Path, required=True, help="JSONL file or directory containing lmsys-chat-1m data")
    parser.add_argument("--output-jsonl", type=Path, required=True, help="Output JSONL file")
    args = parser.parse_args()

    # Load input
    input_data = load_jsonl(args.input_jsonl)

    # Load lmsys-chat-1m dataset
    lmsys_data = {}
    if args.lmsys_chat_1m_paths.is_file():
        files = [args.lmsys_chat_1m_paths]
    else:
        files = list(args.lmsys_chat_1m_paths.glob("*.jsonl"))

    print(f"Loading lmsys-chat-1m data from {len(files)} files...")

    for file in files:
        for item in load_jsonl(file):
            conv_id = item.get("conversation_id")
            if conv_id:
                lmsys_data[conv_id] = item.get("conversation", [])

    # Process and update
    with open(args.output_jsonl, "w", encoding="utf-8") as out_f:
        for item in tqdm(input_data, desc="Processing"):
            metadata: str = item.get("metadata", "")
            metadata_dict = json.loads(metadata) if metadata else {}
            conv_id = metadata_dict.get("conversation_id", "")
            conversation = item.get("messages", [])

            if conversation and conversation[0].get("role") == "user" and not conversation[0].get("content"):
                if conv_id in lmsys_data and lmsys_data[conv_id]:
                    conversation[0]["content"] = lmsys_data[conv_id][0].get("content", "")

            json.dump({
                "conversation_id": conv_id,
                "conversation": conversation,
                "license": item.get("license", ""),
                "generator": item.get("generator", ""),
                "category": item.get("category", ""),
                "reasoning": item.get("reasoning", ""),
            }, out_f, ensure_ascii=False)
            out_f.write("\n")


if __name__ == "__main__":
    main()
