from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Iterable, Tuple
import matplotlib
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, PreTrainedTokenizer


def iter_jsonl(path: Path) -> Iterable[Tuple[int, Dict[str, Any]]]:
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            yield i, json.loads(line)


def batched(it, batch_size: int):
    batch = []
    for x in it:
        batch.append(x)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def count_tokens_batch(
    tokenizer: PreTrainedTokenizer,
    convs: List[List[Dict[str, str]]],
    add_generation_prompt: bool,
) -> List[int]:
    try:
        encoded = tokenizer.apply_chat_template(  # type: ignore
            convs,
            tokenize=True,
            add_generation_prompt=add_generation_prompt,
            add_special_tokens=False,
            return_tensors=None,  # list of input_ids (lists)
        )
        if isinstance(encoded, dict) and "input_ids" in encoded:
            return [len(ids) for ids in encoded["input_ids"]]
        elif isinstance(encoded, list):
            # list of dicts or list of lists
            out = []
            for e in encoded:
                if isinstance(e, dict) and "input_ids" in e:
                    out.append(len(e["input_ids"]))
                else:
                    out.append(len(e))
            return out
        else:
            raise RuntimeError("Unexpected return type from apply_chat_template(tokenize=True)")
    except Exception:
        templated_texts = [
            tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=add_generation_prompt)  # type: ignore
            for c in convs
        ]
        enc = tokenizer(
            templated_texts,
            add_special_tokens=False,
            return_attention_mask=False,
            return_token_type_ids=False,
        )
        return [len(x) for x in enc["input_ids"]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-jsonl", type=Path, required=True)
    p.add_argument("--tokenizer-path", type=str, required=True)
    p.add_argument("--conversation-key", type=str, default="conversation")
    p.add_argument("--template-add-generation-prompt", action="store_true")
    p.add_argument("--plot-path", type=Path, default=None)
    p.add_argument("--show-plot", action="store_true")
    p.add_argument("--max-records", type=int, default=None)
    p.add_argument("--token-limit", type=int, default=32768)
    p.add_argument("--batch-size", type=int, default=512)
    args = p.parse_args()

    if not args.show_plot:
        matplotlib.use("Agg")

    try:
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)
    except Exception as e:
        print(f"[ERROR] Failed to load tokenizer: {e}", file=sys.stderr)
        sys.exit(1)

    tmp_out = args.input_jsonl.with_suffix(".tmp.tokens.jsonl")
    out_f = open(tmp_out, "w", encoding="utf-8")

    processed = 0
    skipped = 0
    over_limit = 0

    collect_for_plot = args.plot_path is not None or args.show_plot
    num_tokens_all: List[int] = [] if collect_for_plot else None

    batch_size = max(1, args.batch_size)
    record_iter = iter_jsonl(args.input_jsonl)
    if args.max_records is not None:
        from itertools import islice

        record_iter = islice(record_iter, args.max_records)

    for batch in batched(record_iter, batch_size):
        idxs, items = zip(*batch)
        convs: List[List[Dict[str, str]]] = []
        valid_mask = []
        for it in items:
            conv = it.get(args.conversation_key)
            if not isinstance(conv, list):
                valid_mask.append(False)
                continue
            valid_mask.append(True)
            convs.append(conv)

        if not any(valid_mask):
            skipped += len(batch)
            continue

        try:
            token_counts = count_tokens_batch(
                tokenizer, convs, add_generation_prompt=args.template_add_generation_prompt
            )
        except Exception:
            token_counts = []
            for conv in convs:
                try:
                    token_counts.extend(count_tokens_batch(tokenizer, [conv], args.template_add_generation_prompt))
                except Exception:
                    token_counts.append(None)

        tc_it = iter(token_counts)
        for vm, it in zip(valid_mask, items):
            if not vm:
                skipped += 1
                continue
            n_tok = next(tc_it)
            if n_tok is None:
                skipped += 1
                continue
            it["num_token"] = int(n_tok)
            if collect_for_plot:
                num_tokens_all.append(int(n_tok))
            if n_tok > args.token_limit:
                over_limit += 1
            out_f.write(json.dumps(it, ensure_ascii=False))
            out_f.write("\n")
            processed += 1

    out_f.close()
    tmp_out.replace(args.input_jsonl)

    print(f"[INFO] Processed: {processed} records, Skipped: {skipped}")
    if over_limit > 0:
        print(f"[INFO] {over_limit} samples exceeded the token limit ({args.token_limit}).")

    if collect_for_plot and processed > 0:
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
