import json
import argparse
import re
from tqdm import tqdm

# <think>thinking_content</think>assistant_output
THINK_PATTERN = re.compile(
    r"^<think>(?P<thinking>.*?)</think>(?P<assistant>.*)$",
    re.DOTALL,
)


def parse_assistant_turn(text: str):
    """
    <think>thinking_content</think>assistant_output の形式のみを受け付ける。
    それ以外は None を返す（不正例）。
    """
    m = THINK_PATTERN.match(text)
    if not m:
        return None, None
    thinking_content = m.group("thinking").strip()
    assistant_output = m.group("assistant").strip()
    return thinking_content, assistant_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--input-target-key", required=True)
    parser.add_argument("--output-target-key", required=True)
    args = parser.parse_args()

    invalid_think_count = 0  # <think> 形式が不正な件数

    with open(args.input_jsonl, "r", encoding="utf-8") as f_in, open(args.output_jsonl, "w", encoding="utf-8") as f_out:
        for line in tqdm(f_in, desc="Processing"):
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)

            # 入力キーがない場合はスキップ
            if args.input_target_key not in data:
                continue

            item = data[args.input_target_key]

            # item = [user_turn, assistant_turn] を想定
            if not isinstance(item, list) or len(item) < 2:
                continue

            user_turn = item[0]
            assistant_turn = item[1]

            # role チェック
            if user_turn.get("role") != "user":
                continue
            if assistant_turn.get("role") != "assistant":
                continue

            user_content = user_turn.get("content", "")
            assistant_content = assistant_turn.get("content", "")

            # user content の長さチェック
            if len(user_content) < 10:
                continue

            # <think>形式の厳密チェック（先頭が <think> で始まらない場合も含め、不正なら捨てる）
            thinking_content, assistant_output = parse_assistant_turn(assistant_content)
            if thinking_content is None:
                invalid_think_count += 1
                continue  # 不正例は捨てる

            # 出力フォーマットを構築
            out_item = [
                {"role": "user", "content": user_content},
                {
                    "role": "assistant",
                    "content": assistant_output,
                    "reasoning_content": thinking_content,
                    "thinking": thinking_content,
                },
            ]

            data_out = {
                args.output_target_key: out_item,
                "uuid": data.get("uuid", ""),
                "generator": data.get("generator", ""),
            }
            f_out.write(json.dumps(data_out, ensure_ascii=False) + "\n")

    # 不正例件数を表示
    print(f"Invalid <think> format examples skipped: {invalid_think_count}")


if __name__ == "__main__":
    main()
