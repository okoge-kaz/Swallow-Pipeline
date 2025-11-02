import argparse
import gzip
import json
import re
import sys
from typing import Any, Dict, Tuple

# ---------- IO helpers ----------


def _open_maybe_gzip(path: str, mode: str):
    """
    Open text file with optional gzip based on file extension.
    mode: "r" or "w" (text mode will be applied)
    """
    if path.endswith(".gz"):
        return gzip.open(path, mode + "t", encoding="utf-8", newline="\n")
    return open(path, mode, encoding="utf-8", newline="\n")


# ---------- reasoning/content extraction ----------


def extract_by_tags(
    text: str, start_tag: str, end_tag: str, keep_tags: bool = False, join_with: str = "\n"
) -> Tuple[str, str]:
    """
    Collect all substrings between <start_tag> and <end_tag> (non-greedy).
    thinking = concatenation of matched contents (tags removed by default)
    content  = original text with matched regions removed (tags removed)
    If no match -> ("", text)
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    pattern = re.compile(re.escape(start_tag) + r"(.*?)" + re.escape(end_tag), flags=re.DOTALL)
    matches = list(pattern.finditer(text))
    if not matches:
        return "", text

    chunks = [m.group(0) if keep_tags else m.group(1) for m in matches]
    thinking = join_with.join(chunks)
    content = pattern.sub("", text)  # remove matched regions (with tags) from content
    return thinking, content


# ---------- main ----------


def main():
    ap = argparse.ArgumentParser(description="Convert JSONL to gpt-oss reasoning format (simple top-level keys).")
    ap.add_argument("--input-jsonl", required=True)
    ap.add_argument("--output-jsonl", required=True)

    # Top-level keys; guaranteed to exist and be strings per user assumption
    ap.add_argument("--question-key", required=True, help="Top-level key for user content (e.g., 'prompt').")
    ap.add_argument("--answer-key", required=True, help="Top-level key for combined reasoning+assistant output.")

    # Tag mode
    ap.add_argument("--reasoning-start-tag", default="<think>", help="Reasoning start tag (default: '<think>').")
    ap.add_argument("--reasoning-end-tag", default="</think>", help="Reasoning end tag (default: '</think>').")
    ap.add_argument(
        "--keep-tags",
        action="store_true",
        help="Keep tags in 'thinking' (content side always removes matched regions).",
    )
    ap.add_argument(
        "--join-multiple-tags-with", default="\n", help="Join string when multiple tag blocks exist (default: newline)."
    )

    # Tokenizer & extras
    ap.add_argument("--tokenizer-dir", required=True, help="HuggingFace tokenizer directory.")
    ap.add_argument(
        "--add-token-counts", action="store_true", help="Add input_token_count/output_token_count using the tokenizer."
    )

    # gpt-oss fields
    ap.add_argument(
        "--model-identity",
        default="You are SwallowLLM, a large language model trained by Swallow Project.",
        help="Value for 'model_identity'.",
    )
    ap.add_argument(
        "--reasoning-effort",
        default="medium",
        choices=["low", "medium", "high", "custom"],
        help="Value for 'reasoning_effort'.",
    )
    ap.add_argument(
        "--builtin-tools",
        nargs="*",
        default=[],
        choices=["browser", "python"],
        help="List of builtin tools to declare (names only).",
    )

    args = ap.parse_args()

    # Load tokenizer (for validation and optional counts)
    try:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_dir, use_fast=True)
    except Exception as e:
        print(f"[ERROR] Failed to load tokenizer from {args.tokenizer_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    total = 0
    converted = 0

    with _open_maybe_gzip(args.input_jsonl, "r") as fin, _open_maybe_gzip(args.output_jsonl, "w") as fout:
        for raw_line in fin:
            line = raw_line.strip()
            if not line:
                continue
            total += 1

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] Skip malformed JSON at line {total}: {e}", file=sys.stderr)
                continue

            # --- Top-level access only (assumed valid & string) ---
            if args.question_key not in obj or args.answer_key not in obj:
                print(
                    f"[WARN] Skip line {total}: missing top-level key(s) {args.question_key!r} or {args.answer_key!r}",
                    file=sys.stderr,
                )
                continue

            user_text = obj[args.question_key]
            combined = obj[args.answer_key]

            if not isinstance(user_text, str):
                user_text = "" if user_text is None else str(user_text)
            if not isinstance(combined, str):
                combined = "" if combined is None else str(combined)

            # Reasoning/content split via tags
            thinking, content = extract_by_tags(
                combined,
                start_tag=args.reasoning_start_tag,
                end_tag=args.reasoning_end_tag,
                keep_tags=args.keep_tags,
                join_with=args.join_multiple_tags_with,
            )

            # If no tags found, content is full answer and thinking is ""
            out: Dict[str, Any] = {
                "builtin_tools": args.builtin_tools or [],
                "model_identity": args.model_identity,
                "reasoning_effort": args.reasoning_effort,
                "messages": [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "thinking": thinking, "content": content},
                ],
            }

            # Optional token counts (assistant.content only)
            if args.add_token_counts:
                try:
                    in_ids = tokenizer(user_text, add_special_tokens=False).input_ids
                    out_ids = tokenizer(content, add_special_tokens=False).input_ids
                    out["input_token_count"] = len(in_ids)
                    out["output_token_count"] = len(out_ids)
                except Exception as e:
                    print(f"[WARN] Token counting failed at line {total}: {e}", file=sys.stderr)

            fout.write(json.dumps(out, ensure_ascii=False) + "\n")  # type: ignore
            converted += 1

    print(f"[DONE] Converted {converted}/{total} lines.", file=sys.stderr)


if __name__ == "__main__":
    main()
