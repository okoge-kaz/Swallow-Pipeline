import argparse
import json
import gzip
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Any, Dict, IO, Iterable, List, cast
from transformers import AutoTokenizer, PreTrainedTokenizer


def _open_maybe_gzip(path: Path, mode: str):
    # mode: "r" or "w" (text mode will be applied)
    if str(path).endswith(".gz"):
        return gzip.open(path, mode + "t", encoding="utf-8", newline="\n")
    return open(path, mode, encoding="utf-8", newline="\n")


def _iter_jsonl(fp: IO[str]) -> Iterable[str]:
    # Yield raw non-empty lines (keep order & allow very large files)
    for line in fp:
        line = line.rstrip("\n")
        if not line.strip():
            # skip empty lines
            continue
        yield line


def _extract_messages(item: Any, *, idx: int) -> List[Dict[str, Any]]:
    """
    Allow either:
      - dict with key "messages": list[dict]
      - list[dict] (messages directly)
    """
    if isinstance(item, dict):
        if "messages" not in item:
            raise TypeError(f"Item {idx}: dict must contain 'messages' key.")
        msgs = item["messages"]
    elif isinstance(item, list):
        msgs = item
    else:
        raise TypeError(f"Item {idx}: must be a dict(with 'messages') or a list of messages.")

    if not isinstance(msgs, list):
        raise TypeError(f"Item {idx}: 'messages' must be a list.")
    return msgs  # type: ignore[return-value]


def main():
    ap = argparse.ArgumentParser(
        description="Apply chat template to a JSONL (one item per line) and add/update `text` per item."
    )
    ap.add_argument("--input-jsonl", required=True, type=Path, help="Path to .jsonl or .jsonl.gz")
    ap.add_argument("--tokenizer-dir", required=True, help="HF tokenizer dir or repo id")
    ap.add_argument("--add-generation-prompt", action="store_true")
    ap.add_argument("--trust-remote-code", action="store_true")
    ap.add_argument("--skip-if-exists", action="store_true", help="Skip if item already has `text`")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.tokenizer_dir, trust_remote_code=args.trust_remote_code)
    tok = cast(PreTrainedTokenizer, tok)

    src = args.input_jsonl
    if not src.exists():
        print(f"Input not found: {src}", file=sys.stderr)
        sys.exit(1)

    # Prepare temp output in the same directory for atomic replace
    fd, tmp = tempfile.mkstemp(prefix=src.name + ".", dir=str(src.parent))
    os.close(fd)
    tmp_path = Path(tmp)

    total = 0
    updated = 0

    try:
        with _open_maybe_gzip(src, "r") as fin, _open_maybe_gzip(tmp_path, "w") as fout:
            for i, raw in enumerate(_iter_jsonl(fin), 1):
                total += 1
                try:
                    item = json.loads(raw)
                except Exception as e:
                    raise ValueError(f"Invalid JSON at line {i}: {e}")

                if isinstance(item, dict) and "text" in item and args.skip_if_exists:
                    # write unchanged (re-dump may reformat, but content equivalent)
                    json.dump(item, fout, ensure_ascii=False)
                    fout.write("\n")
                    continue

                # Compute messages & render
                msgs = _extract_messages(item, idx=i)
                try:
                    rendered = tok.apply_chat_template(
                        conversation=msgs,
                        tokenize=False,
                        model_identity=item.get("model_identity") if isinstance(item, dict) else None,
                        add_generation_prompt=args.add_generation_prompt
                    )
                except Exception as e:
                    raise RuntimeError(f"apply_chat_template failed at line {i}: {e}")

                # Ensure dict so we can attach "text"
                if not isinstance(item, dict):
                    # If original was list[messages], convert to dict with messages + text
                    item = {"messages": msgs}

                item["text"] = rendered
                updated += 1

                json.dump(item, fout, ensure_ascii=False)
                fout.write("\n")

    except Exception:
        # Clean up temp on any failure before move
        tmp_path.unlink(missing_ok=True)
        raise

    # Atomic replace
    shutil.move(str(tmp_path), str(src))
    print(f"Done. items: {total}, updated: {updated}", file=sys.stderr)


if __name__ == "__main__":
    main()
