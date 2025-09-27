#!/bin/bash

source .venv/bin/activate

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1_code.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/code-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/code-jsonl/merge_train.jsonl \
  --verbose
