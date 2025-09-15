import argparse
import json
from pathlib import Path


def split_jsonl_by_score(
    input_dir: str, output_dir: str, score_key: str, model_name: str, thresholds: list[int]
) -> None:
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process each file matching the pattern
    for file_path in Path(input_dir).glob(f"train_*_{model_name}.jsonl"):
        # Initialize output files
        base_name = file_path.stem
        low_file = Path(output_dir) / f"{base_name}_low_{model_name}.json"
        medium_file = Path(output_dir) / f"{base_name}_medium_{model_name}.json"
        high_file = Path(output_dir) / f"{base_name}_high_{model_name}.json"

        with (
            open(low_file, "w", encoding="utf-8") as low_f,
            open(medium_file, "w", encoding="utf-8") as medium_f,
            open(high_file, "w", encoding="utf-8") as high_f,
        ):
            # Read input file
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        score = data.get(score_key, 0)

                        # Determine which file to write to based on score
                        if 0 <= score <= thresholds[0]:
                            low_f.write(json.dumps(data) + "\n")
                        elif 3 <= score <= thresholds[1]:
                            medium_f.write(json.dumps(data) + "\n")
                        elif 7 <= score <= thresholds[2]:
                            high_f.write(json.dumps(data) + "\n")
                    except json.JSONDecodeError:
                        print(f"Warning: Skipping invalid JSON line in {file_path}")
                        continue


def main() -> None:
    parser = argparse.ArgumentParser(description="Split JSONL files by score ranges.")

    parser.add_argument("--input-dir", required=True, help="Input directory containing JSONL files")
    parser.add_argument("--output-dir", required=True, help="Output directory for split files")

    parser.add_argument("--input-jsonl-key", type=str, default="score", help="Key to use for score in JSONL files")
    parser.add_argument("--scoring-model", type=str, default="Qwen3-14B", help="Scoring model name")

    parser.add_argument(
        "--score-thresholds", nargs=3, type=int, default=[2, 6, 10], help="Score thresholds for low, medium, high"
    )
    args = parser.parse_args()

    split_jsonl_by_score(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        score_key=args.input_jsonl_key,
        model_name=args.scoring_model,
        thresholds=args.score_thresholds,
    )


if __name__ == "__main__":
    main()
