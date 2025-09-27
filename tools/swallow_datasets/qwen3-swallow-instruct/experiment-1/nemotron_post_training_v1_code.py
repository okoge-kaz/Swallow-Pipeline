import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from tqdm import tqdm
from datasets import load_dataset


def load_jsonl(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(items, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            json.dump(it, f, ensure_ascii=False)
            f.write("\n")


def get_field(item: Dict[str, Any], key: str) -> Optional[Any]:
    """Find key in item, or in metadata/meta subdict."""
    if key in item:
        return item[key]
    meta = json.loads(item.get("metadata", "{}")) if "metadata" in item else {}
    return meta.get(key)


# Lazy-loaded datasets cache
_ds_cache: Dict[str, Any] = {}


def get_dataset(ds_name: str):
    if ds_name not in _ds_cache:
        if ds_name == "taco":
            _ds_cache[ds_name] = load_dataset("BAAI/TACO", trust_remote_code=True)
        elif ds_name == "apps":
            _ds_cache[ds_name] = load_dataset("codeparrot/apps", trust_remote_code=True)
        elif ds_name == "code_contests":
            _ds_cache[ds_name] = load_dataset("deepmind/code_contests")
        elif ds_name == "open-r1/codeforces":
            _ds_cache[ds_name] = load_dataset("open-r1/codeforces")
        else:
            raise ValueError(f"Unsupported dataset: {ds_name}")
    return _ds_cache[ds_name]


def build_question_from_example(ds_name: str, example: Dict[str, Any]) -> Optional[str]:
    """Replicates the logic from your original script."""
    if ds_name == "code_contests":
        desc = example.get("description")
        return desc if desc else None

    if ds_name in ["taco", "apps"]:
        return example.get("question")

    if ds_name == "open-r1/codeforces":
        if not example.get("description"):
            return None
        parts = [example["description"]]

        if example.get("input_format"):
            parts.append("\n\nInput\n\n" + example["input_format"])
        if example.get("output_format"):
            parts.append("\n\nOutput\n\n" + example["output_format"])
        if example.get("examples"):
            parts.append("\n\nExamples")
            for ex in example["examples"]:
                if "input" in ex and ex["input"] is not None:
                    parts.append("\n\nInput\n\n" + str(ex["input"]))
                if "output" in ex and ex["output"] is not None:
                    parts.append("\n\nOutput\n\n" + str(ex["output"]))
        if example.get("note"):
            parts.append("\n\nNote\n\n" + example["note"])
        return "".join(parts)

    return None


def fetch_question(ds_name: str, split: str, index: int) -> Optional[str]:
    ds = get_dataset(ds_name)
    # Defensive: ensure index in range
    if split not in ds:
        raise KeyError(f"Split '{split}' not found in dataset '{ds_name}'. Available: {list(ds.keys())}")
    split_ds = ds[split]
    if not (0 <= index < len(split_ds)):
        raise IndexError(f"Index {index} out of range for {ds_name}[{split}] (len={len(split_ds)}).")
    example = split_ds[int(index)]
    return build_question_from_example(ds_name, example)


def process_item(item: Dict[str, Any], strict_role_check: bool = True, verbose: bool = False) -> Dict[str, Any]:
    """Replace messages[0].content == '-' with fetched question."""
    messages = item.get("messages")
    if not isinstance(messages, list) or len(messages) == 0 or not isinstance(messages[0], dict):
        if verbose:
            print("[WARN] Skipping: messages[0] missing or invalid", file=sys.stderr)
        return item

    m0 = messages[0]
    role_ok = (m0.get("role") == "user") if strict_role_check else True
    if not role_ok or m0.get("content") != "-":
        # Nothing to replace
        return item

    ds_name = get_field(item, "dataset")
    ds_split = get_field(item, "split")
    ds_index = get_field(item, "index")

    if ds_name is None or ds_split is None or ds_index is None:
        if verbose:
            print("[WARN] Missing dataset/split/index; cannot replace content", file=sys.stderr)
        return item

    try:
        q = fetch_question(str(ds_name), str(ds_split), int(ds_index))
        if q is None or len(q.strip()) == 0:
            if verbose:
                print(f"[WARN] Empty question for {ds_name} {ds_split} {ds_index}", file=sys.stderr)
            return item
        # Replace content
        m0["content"] = q
        # Ensure tool_calls key exists as list (as in your example). Leave as-is if present.
        if "tool_calls" not in m0 or not isinstance(m0["tool_calls"], list):
            m0["tool_calls"] = []
    except Exception as e:
        if verbose:
            print(f"[ERROR] {ds_name} {ds_split} {ds_index}: {e.__class__.__name__}: {e}", file=sys.stderr)

    return item


def main():
    ap = argparse.ArgumentParser(description="Replace messages[0].content '-' with fetched question text.")
    ap.add_argument("--input-jsonl", type=Path, required=True)
    ap.add_argument("--output-jsonl", type=Path, required=True)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    processed = []
    for it in tqdm(load_jsonl(args.input_jsonl), desc="Processing"):
        processed.append(process_item(it, strict_role_check=True, verbose=args.verbose))

    write_jsonl(processed, args.output_jsonl)


if __name__ == "__main__":
    main()
