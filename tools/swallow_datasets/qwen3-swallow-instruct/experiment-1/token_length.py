import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

import matplotlib
import matplotlib.pyplot as plt

from transformers import AutoTokenizer, PreTrainedTokenizer


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(items: List[Dict[str, Any]], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            json.dump(it, f, ensure_ascii=False)
            f.write("\n")


def count_tokens_with_template(
    tokenizer: PreTrainedTokenizer,
    conversation: List[Dict[str, str]],
    add_generation_prompt: bool = False,
) -> int:
    """
    conversation: [{"role": "system|user|assistant|tool", "content": "..."}]
    """
    try:
        templated_text: str = tokenizer.apply_chat_template(  # type: ignore
            conversation,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
        )
    except Exception as e:
        raise RuntimeError(
            f"apply_chat_template failed: {e}. "
            f"Check that your tokenizer has a chat template and the conversation schema is correct."
        )

    enc = tokenizer(
        templated_text,
        add_special_tokens=False,
        return_attention_mask=False,
        return_token_type_ids=False,
    )
    return len(enc["input_ids"])  # type: ignore


def main():
    parser = argparse.ArgumentParser(
        description="Apply chat template to conversation and add num_token to each JSONL record."
    )
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--tokenizer-path", type=str, required=True)
    parser.add_argument(
        "--conversation-key", type=str, default="conversation", help="Key name that stores chat messages list"
    )
    parser.add_argument(
        "--template-add-generation-prompt",
        action="store_true",
        help="Pass add_generation_prompt=True to apply_chat_template",
    )
    parser.add_argument(
        "--plot-path", type=Path, default=None, help="If set, save histogram image to this path (e.g., tokens_hist.png)"
    )
    parser.add_argument("--show-plot", action="store_true", help="Show histogram window (may require GUI environment)")
    parser.add_argument("--max-records", type=int, default=None, help="Process only first N records for quick tests")
    parser.add_argument(
        "--token-limit",
        type=int,
        default=32768,
        help="Warn if any sample has more tokens than this limit (default=32768)",
    )
    args = parser.parse_args()

    if not args.show_plot:
        matplotlib.use("Agg")

    try:
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)
    except Exception as e:
        print(f"[ERROR] Failed to load tokenizer from '{args.tokenizer_path}': {e}", file=sys.stderr)
        sys.exit(1)

    data = load_jsonl(args.input_jsonl)
    if args.max_records is not None:
        data = data[: args.max_records]

    num_tokens_all: List[int] = []
    processed: List[Dict[str, Any]] = []

    skipped = 0
    over_limit = 0
    for idx, item in enumerate(data):
        if args.conversation_key not in item:
            skipped += 1
            continue

        conv = item[args.conversation_key]
        if not isinstance(conv, list):
            skipped += 1
            continue

        try:
            n_tok = count_tokens_with_template(
                tokenizer,
                conv,
                add_generation_prompt=args.template_add_generation_prompt,
            )
        except Exception as e:
            print(f"[WARN] Skipping idx={idx} due to template/tokenize error: {e}", file=sys.stderr)
            skipped += 1
            continue

        item["num_token"] = int(n_tok)
        num_tokens_all.append(n_tok)
        processed.append(item)

        if n_tok > args.token_limit:
            print(
                f"[WARNING] Record idx={idx} has {n_tok} tokens (exceeds {args.token_limit})",
                file=sys.stderr,
                flush=True,
            )
            over_limit += 1

    write_jsonl(processed, args.input_jsonl)

    print(f"[INFO] Processed: {len(processed)} records, Skipped: {skipped}")
    if over_limit > 0:
        print(f"[INFO] {over_limit} samples exceeded the token limit ({args.token_limit}).")

    if len(num_tokens_all) == 0:
        print("[INFO] No records to plot. Done.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(num_tokens_all, bins="auto")
    plt.xlabel("Number of tokens")
    plt.ylabel("Number of samples")

    if args.plot_path is not None:
        args.plot_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.plot_path, dpi=150, bbox_inches="tight")
        print(f"[INFO] Saved histogram: {args.plot_path}")

    if args.show_plot:
        plt.show()

    plt.close()


if __name__ == "__main__":
    main()
