#!/bin/bash

set -euo pipefail
source .venv/bin/activate

INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v2/data-jsonl
OUTPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v2/multilingual_ja

mkdir -p "$OUTPUT_DIR"

for i in $(seq -w 0 36); do
    in_file=$INPUT_DIR/multilingual_ja-000${i}-of-00037.jsonl
    out_file=$OUTPUT_DIR/train-000${i}-of-00037.jsonl

    echo "[INFO] Processing $in_file -> $out_file"
    python tools/public_datasets/nemotron-post-training-v2/multilingual.py \
        --input-jsonls "$in_file" \
        --output-jsonl "$out_file" \
        --verbose
done

echo "[INFO] All files processed successfully."
