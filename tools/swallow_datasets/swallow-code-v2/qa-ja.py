import argparse
import json
from pathlib import Path
import sys

def process(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    lines_in = 0
    lines_out = 0
    errors = 0

    with input_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:
        for lineno, line in enumerate(fin, 1):
            line = line.strip()
            if not line:
                continue
            lines_in += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] Skip line {lineno}: JSON decode error: {e}", file=sys.stderr)
                errors += 1
                continue

            q = item.get("question", "")
            a = item.get("answer", "")

            text = f"{q}\n\n```python\n{a}\n```"

            out_obj = {"text": text}
            fout.write(json.dumps(out_obj, ensure_ascii=False))
            fout.write("\n")
            lines_out += 1

    print(f"[INFO] Done. Read {lines_in} lines, wrote {lines_out} lines, {errors} errors.", file=sys.stderr)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build JSONL with {'text': question + '\\n\\n```python\\n' + answer + '\\n```'} from input JSONL."
    )
    parser.add_argument("--input-jsonl", type=Path, required=True, help="Path to input JSONL file.")
    parser.add_argument("--output-jsonl", type=Path, required=True, help="Path to output JSONL file.")
    args = parser.parse_args()
    process(args.input_jsonl, args.output_jsonl)

if __name__ == "__main__":
    main()
