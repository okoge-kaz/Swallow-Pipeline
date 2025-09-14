import argparse
import json
from pathlib import Path


def process_jsonl_file(input_file: Path, output_file: Path, mode: str) -> None:
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    processed_count = 0
    filtered_count = 0
    error_count = 0

    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_file, "w", encoding="utf-8") as outfile,
    ):
        for line_num, line in enumerate(infile, 1):
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            try:
                data = json.loads(line)
                if "input" not in data or "output" not in data:
                    print(f"Error: {line_num} missing 'input' or 'output' field")
                    error_count += 1
                    continue

                if "input" in data:
                    data["question"] = (
                        data.pop("input")
                        .replace(
                            "Solve the following problem. Make sure to put the answer (and only answer) inside \\boxed{}.",
                            "",
                        )
                        .strip()
                    )
                if "output" in data:
                    data["r1_generation"] = data.pop("output")
                    # remove <think> ... </think> content if exists
                    r1_generation: str = data["r1_generation"]
                    if "<think>" in r1_generation and "</think>" in r1_generation:
                        start = r1_generation.index("<think>")
                        end = r1_generation.index("</think>")
                        data["solution"] = (
                            r1_generation[:start] + r1_generation[end:]
                        ).strip()
                    else:
                        data["solution"] = r1_generation

                # construct text based on mode
                if mode == "solution":
                    text_content = (
                        "Question:\n\n"
                        + str(data["question"])
                        + "\n\nSolution:\n\n"
                        + str(data["solution"])
                    )
                else:  # r1_generation
                    text_content = (
                        "Question:\n\n"
                        + str(data["question"])
                        + "\n\nSolution:\n\n"
                        + str(data["r1_generation"])
                    )

                output_data = data.copy()
                output_data["text"] = text_content

                outfile.write(json.dumps(output_data, ensure_ascii=False) + "\n")
                processed_count += 1

            except json.JSONDecodeError as e:
                print(f"Error: {line_num} raw is not valid JSON: {e}")
                error_count += 1
                continue
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                error_count += 1
                continue

    print(f"  - Processed (judgement=='right'): {processed_count} raw")
    print(f"  - Filtered Out (judgement!='right'): {filtered_count} raw")
    print(f"  - Error: {error_count} raw")
    print(f"  - Output dir: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="extract and process JSONL data where judgement=='right'"
    )
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument(
        "--mode",
        required=True,
        choices=["solution", "r1_generation"],
        help="choose whether to use 'solution' or 'r1_generation' field for Solution text",
    )

    args = parser.parse_args()

    try:
        process_jsonl_file(args.input_jsonl, args.output_jsonl, args.mode)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
