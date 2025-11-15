import argparse
import json
from typing import List, Dict, Any

from transformers import AutoTokenizer, PreTrainedTokenizer

FORBIDDEN_TAGS = {
    "<|start|>",
    "<|message|>",
    "<|end|>",
    "<|channel|>",
    "<|return|>",
}


def contains_invalid_tag(conversation: list[dict[str, str]]) -> bool:
    for turn in conversation:
        for k, v in turn.items():
            if k not in {"content", "reasoning_content", "thinking"}:
                # tool_calls, role
                continue

            if not isinstance(v, str):
                print(f"Found non-string value in turn: {turn}")
                return True
            if len(v) < 1:
                print(f"Found empty value in turn: {turn}")
                return True

            for tag in FORBIDDEN_TAGS:
                if tag in v:
                    print(f"Found forbidden tag {tag} in value: {v}")
                    return True
    return False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=str, required=True)
    parser.add_argument("--output-jsonl", type=str, required=True)
    parser.add_argument("--input-target-key", type=str, required=True)

    # tokenizer names
    parser.add_argument("--qwen3-tokenizer", type=str, required=True)
    parser.add_argument("--gpt-oss-tokenizer", type=str, required=True)

    # gpt-oss
    parser.add_argument("--reasoning-effort", type=str, default="medium")
    parser.add_argument(
        "--model-identity", type=str, default="You are ChatGPT, a large language model trained by OpenAI."
    )

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


def apply_gpt_oss_batch(
    tokenizer: PreTrainedTokenizer,
    conversations_buffer: list[list[dict[str, str]]],
    reasoning_effort: str,
    model_identity: str,
) -> List[str]:
    prompts = tokenizer.apply_chat_template(
        conversation=conversations_buffer,
        tokenize=False,
        reasoning_effort=reasoning_effort,
        model_identity=model_identity,
    )
    if isinstance(prompts, str):
        prompts = [prompts]
    return prompts  # type: ignore


def main():
    args = parse_args()
    qwen3_tokenizer = AutoTokenizer.from_pretrained(args.qwen3_tokenizer)
    gpt_oss_tokenizer = AutoTokenizer.from_pretrained(args.gpt_oss_tokenizer)

    with (
        open(args.input_jsonl, "r", encoding="utf-8") as infile,
        open(args.output_jsonl, "w", encoding="utf-8") as outfile,
    ):
        buffer: List[Dict[str, Any]] = []
        conversation_buffer: list[list[dict[str, str]]] = []
        invalid_count = 0

        def flush_buffer():
            nonlocal buffer, conversation_buffer
            if not buffer:
                return

            qwen3_prompts = apply_qwen3_batch(qwen3_tokenizer, conversation_buffer)
            gpt_oss_prompts = apply_gpt_oss_batch(
                gpt_oss_tokenizer,
                conversation_buffer,
                args.reasoning_effort,
                args.model_identity,
            )

            assert len(buffer) == len(qwen3_prompts) == len(gpt_oss_prompts)

            for rec, p_qwen3, p_gptoss in zip(buffer, qwen3_prompts, gpt_oss_prompts):
                rec["text_qwen3"] = p_qwen3
                rec["text_gpt_oss"] = p_gptoss
                outfile.write(json.dumps(rec, ensure_ascii=False) + "\n")

            buffer = []
            conversation_buffer = []

        for line in infile:
            try:
                item = json.loads(line.strip())
            except json.JSONDecodeError:
                invalid_count += 1
                continue

            if args.input_target_key not in item:
                raise KeyError(f"{args.input_target_key} not in record: {item}")

            if args.input_target_key in item and len(item[args.input_target_key]) == 2:
                conversation = item[args.input_target_key]

                if (
                    "thinking" not in item[args.input_target_key][1]
                    and "reasoning_content" in item[args.input_target_key][1]
                ):
                    # for Okazaki Lab style
                    item[args.input_target_key][1]["thinking"] = item[args.input_target_key][1]["reasoning_content"]
                if contains_invalid_tag(conversation):
                    invalid_count += 1
                    continue

                buffer.append(item)
                conversation_buffer.append(conversation)

                if len(buffer) >= args.batch_size:
                    flush_buffer()

    print(f"Total invalid records skipped: {invalid_count}")

if __name__ == "__main__":
    main()
