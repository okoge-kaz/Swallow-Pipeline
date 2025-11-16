import argparse
import json
import os
import glob


def has_refusal(text: str) -> bool:
    """gpt-oss が拒否しているっぽい文を検出（大文字小文字無視）"""
    lower = text.lower()
    patterns = [
        "i'm sorry, but i can't",
        "i'm sorry but i can't",
        "i'm sorry, i can't",
        "i am sorry, but i can't",
        "i am sorry but i can't",
        "i cannot help with that",
        "i can't help with that",
        "i can’t help with that",
        "i can't assist with that",
        "i can’t assist with that",
        "as an ai language model",
        "i am not able to",
        "i'm not able to",
        "i’m not able to",
        "i'm unable to",
        "i’m unable to",
    ]
    return any(p in lower for p in patterns)


def has_invalid_meta(text: str) -> bool:
    """翻訳プロンプトやメタ文を検出"""
    jp_patterns = [
        "以下の文を日本語に翻訳してください",
        "以下の文を日本語に訳してください",
        "以下の文章を日本語に翻訳してください",
        "以下を日本語に翻訳してください",
        "以下を日本語に訳してください",
        "日本語に翻訳してください",
        "日本語に訳してください",
        "日本語に翻訳します",
        "日本語に訳します",
        "翻訳します。",
        "翻訳いたします",
        "翻訳していきます",
    ]

    en_patterns = [
        "here is the translation",
        "here's the translation",
        "here is my translation",
        "i will translate",
        "let me translate",
        "the translation is",
        "translation:",
    ]

    lower = text.lower()
    if any(p in text for p in jp_patterns):
        return True
    if any(p in lower for p in en_patterns):
        return True

    return False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str, required=True)
    parser.add_argument("--output-jsonl", type=str, required=True)
    parser.add_argument("--input-target-key", type=str, required=True)  # e.g., "conversation"
    return parser.parse_args()


def main():
    args = parse_args()

    jsonl_paths = sorted(glob.glob(os.path.join(args.input_dir, "*.jsonl")))

    total_count = 0
    kept_count = 0
    empty_count = 0
    over_refusal_count = 0
    invalid_count = 0

    with open(args.output_jsonl, "w", encoding="utf-8") as fw:
        for path in jsonl_paths:
            with open(path, "r", encoding="utf-8") as fr:
                for line in fr:
                    line = line.strip()
                    if not line:
                        continue
                    total_count += 1

                    try:
                        sample = json.loads(line)
                    except json.JSONDecodeError:
                        invalid_count += 1
                        continue

                    if args.input_target_key not in sample:
                        invalid_count += 1
                        continue

                    conversation = sample[args.input_target_key]
                    if not isinstance(conversation, list) or len(conversation) == 0:
                        invalid_count += 1
                        continue

                    first = conversation[0]
                    if not isinstance(first, dict):
                        invalid_count += 1
                        continue

                    role = first.get("role", "")
                    content = first.get("content", "")
                    content = "" if content is None else str(content)

                    # ---- 1. empty チェック ----
                    if len(content.strip()) == 0:
                        empty_count += 1
                        continue

                    # ---- 2. 拒否文チェック ----
                    if has_refusal(content):
                        over_refusal_count += 1
                        continue

                    # ---- 3. メタ文チェック ----
                    if has_invalid_meta(content):
                        invalid_count += 1
                        continue

                    # OK → 書き出し
                    fw.write(json.dumps(sample, ensure_ascii=False) + "\n")
                    kept_count += 1

    # 統計表示
    print(f"Total: {total_count}")
    print(f"Kept: {kept_count}")
    print(f"empty_count: {empty_count}")
    print(f"over_refusal_count: {over_refusal_count}")
    print(f"invalid_count: {invalid_count}")


if __name__ == "__main__":
    main()
