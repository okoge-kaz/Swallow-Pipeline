#!/bin/bash

SCRIPT_DIR=/groups/gag51395/fujii/src/Swallow-Pipeline
cd $SCRIPT_DIR

DATASET_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public

source .venv/bin/activate

# Nemotron Post Training v1 Math
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v1/math-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-math.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v1-Math" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"

# Nemotron Post Training v1 STEM
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v1/stem-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-stem.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v1-STEM" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"

# Nemotron Post Training v1 Code
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v1/code-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-code.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v1-Code" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"

# Nemotron Post Training v2 Math
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v2/math-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-math.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v2-Math" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"

# Nemotron Post Training v2 STEM
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v2/stem-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-stem.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v2-STEM" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"

# Nemotron Post Training v2 Code
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_v1.py \
  --input-jsonl $DATASET_DIR/Nemotron-Post-Training-Dataset-v2/code-jsonl/train.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-code.jsonl \
  --dataset-name "Nemotron-Post-Training-Dataset-v2-Code" \
  --former-jsonl-key "messages" \
  --new-jsonl-key "conversation"
