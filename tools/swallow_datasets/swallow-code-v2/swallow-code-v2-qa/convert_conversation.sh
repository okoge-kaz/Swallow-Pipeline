#!/bin/bash

source .venv/bin/activate

INPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-code-v2-dev/qa/python/medium_quality/Qwen3-30B-A3B-Instruct-2507-FP8"
OUTPUT_DIR=$INPUT_DIR/conversation
mkdir -p $OUTPUT_DIR

python tools/swallow_datasets/swallow-code-v2/swallow-code-v2-qa/convert_conversation.py \
  --input-dir $INPUT_DIR \
  --output-dir $OUTPUT_DIR

