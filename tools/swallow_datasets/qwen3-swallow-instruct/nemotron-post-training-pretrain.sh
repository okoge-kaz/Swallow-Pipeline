#!/bin/bash

source .venv/bin/activate


# Nemotron-Post-Training Code DeepSeek R1
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-code-deepseek-r1-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

# Nemotron-Post-Training Code gpt-oss
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/code-jsonl/gpt-oss-120b/medium
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-code-gpt-oss-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

##################################################################

# Nemotron-Post-Training Math DeepSeek R1
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-deepseek-r1-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

# Nemotron-Post-Training Math gpt-oss
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/math-jsonl/gpt-oss-120b/medium
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

##################################################################

# Nemotron-Post-Training Science DeepSeek R1
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science/pretrain/nemotron-post-training-v1-science-deepseek-r1-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

# Nemotron-Post-Training Math gpt-oss
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/swallow-sft-reasoning/stem/gpt-oss-120b/medium/
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."
