#!/bin/sh

SCRIPT_DIR=/groups/gag51395/fujii/src/Swallow-Pipeline

cd ${SCRIPT_DIR}
source .ven/bin/activate

DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${DATASET_DIR}/merged.jsonl \
  --output-jsonl ${DATASET_DIR}/train.jsonl

DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp5

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${DATASET_DIR}/merged.jsonl \
  --output-jsonl ${DATASET_DIR}/train.jsonl

DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp6

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${DATASET_DIR}/merged-ja-min.jsonl \
  --output-jsonl ${DATASET_DIR}/train-ja-min.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${DATASET_DIR}/merged-ja-max.jsonl \
  --output-jsonl ${DATASET_DIR}/train-ja-max.jsonl
