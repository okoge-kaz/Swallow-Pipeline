#!/bin/bash

source .venv/bin/activate

# Nemotron Post-Training v1 code
DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/code-jsonl
OUTPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-convert.py \
  --input-jsonl $DATASET_DIR/merge_train.jsonl \
  --output-jsonl $OUTPUT_DIR/code/nemotron-post-training-v1-code-deepseek-r1.jsonl \
  --input-target-key messages \
  --output-target-key conversation

# Nemotron Post-Training v1 math
DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/math-jsonl
OUTPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-convert.py \
  --input-jsonl $DATASET_DIR/train.jsonl \
  --output-jsonl $OUTPUT_DIR/math/nemotron-post-training-v1-math-deepseek-r1.jsonl \
  --input-target-key messages \
  --output-target-key conversation

# Nemotron Post-Training v1 science
DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/swallow-sft-reasoning/stem
OUTPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-convert.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v1-stem-en-deduplicated.jsonl \
  --output-jsonl $OUTPUT_DIR/science/nemotron-post-training-v1-science-deepseek-r1.jsonl \
  --input-target-key conversation \
  --output-target-key conversation
