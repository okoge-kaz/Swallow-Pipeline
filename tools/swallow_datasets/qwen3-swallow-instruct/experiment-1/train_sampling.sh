#!/bin/sh

SCRIPT_DIR=/groups/gag51395/fujii/src/Swallow-Pipeline

cd ${SCRIPT_DIR}
source .ven/bin/activate

# Nemotron Post Training v1 Code <=32k 200k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-code.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-code-32k-200k.jsonl \
  --max-tokens 32768 \
  --num-samples 200000

# Nemotron Post Training v1 Math <=32k 200k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-math.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-math-32k-200k.jsonl \
  --max-tokens 32768 \
  --num-samples 200000

# Nemotron Post Training v1 STEM <=32k 100k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-stem-deduplicated.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-stem-32k-100k.jsonl \
  --max-tokens 32768 \
  --num-samples 100000
