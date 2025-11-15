import argparse
import json
import glob
import os
from typing import List, Dict, Any

from transformers import AutoTokenizer, PreTrainedTokenizer



def contains_invalid_tag(conversation: list[dict[str, str]]) -> bool:
    for turn in conversation:
        for k, v in turn.items():
            if k not in {"content"}:
                # tool_calls, role
                continue

            if not isinstance(v, str):
                print(f"Found non-string value in turn: {turn}")
                return True
            if len(v) < 1:
                print(f"Found empty value in turn: {turn}")
                return True

    return False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str, required=True)
    parser.add_argument("--output-jsonl", type=str, required=True)
    parser.add_argument("--input-target-key", type=str, required=True)

    # tokenizer names
    parser.add_argument("--qwen3-tokenizer", type=str, required=True)

    parser.add_argument("--batch-size", type=int, default=64)

    return parser.parse_args()


def apply_qwen3_batch(
    tokenizer: PreTrainedTokenizer,
    conversations_buffer: list[list[dict[str, str]]],
) -> List[str]:
    prompts = tokenizer.apply_chat_template(
        conversations_buffer,
        tokenize=False,
    )
    if isinstance(prompts, str):
        prompts = [prompts]
    return prompts  # type: ignore


def main():
    args = parse_args()

    qwen3_tokenizer = AutoTokenizer.from_pretrained(args.qwen3_tokenizer)

    input_files = sorted(glob.glob(os.path.join(args.input_dir, "*.jsonl")))
    if not input_files:
        raise FileNotFoundError(f"No jsonl files found in {args.input_dir}")

    with open(args.output_jsonl, "w", encoding="utf-8") as fout:
        buffer: List[Dict[str, Any]] = []
        conversation_buffer: list[list[dict[str, str]]] = []

        def flush_buffer():
            nonlocal buffer, conversation_buffer
            if not buffer:
                return

            qwen3_prompts = apply_qwen3_batch(qwen3_tokenizer, conversation_buffer)
            assert len(buffer) == len(qwen3_prompts)

            for rec, p_qwen3 in zip(buffer, qwen3_prompts):
                rec["text_qwen3"] = p_qwen3
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

            buffer = []
            conversation_buffer = []

        invalid_count = 0

        for fname in input_files:
            with open(fname, "r", encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)

                    if args.input_target_key not in rec:
                        raise KeyError(f"{args.input_target_key} not in record: {rec}")

                    conversation = rec[args.input_target_key]
                    rec[args.input_target_key][1]["thinking"] = ""
                    rec[args.input_target_key][1]["reasoning_content"] = ""
                    if contains_invalid_tag(conversation):
                        invalid_count += 1
                        continue

                    buffer.append(rec)
                    conversation_buffer.append(conversation)

                    if len(buffer) >= args.batch_size:
                        flush_buffer()

        flush_buffer()
    print(f"Total invalid records skipped: {invalid_count}")


if __name__ == "__main__":
    main()
