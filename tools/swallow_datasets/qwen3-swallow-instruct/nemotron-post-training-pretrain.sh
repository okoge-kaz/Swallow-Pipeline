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
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science/pretrain/nemotron-post-training-v1-science-gpt-oss-model-identity-chat-gpt.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

#################################################################

# lmsys-chat-1m (Japanese) okazaki lab
INPUT_DIR=/groups/gag51395/datasets/instruct/lmsys-chat-1m/sft
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt.jsonl

mkdir -p $(dirname $OUTPUT_PATH)

python tools/swallow_datasets/qwen3-swallow-instruct/lmsys-chat-1m-convert.py \
  --input-jsonl $INPUT_DIR/lmsys-chat-1m_synthesized_single-turn_conversation_gpt-oss-medium_sft-wo-pii-and-template-instructions.jsonl \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI." \
  --reasoning-effort "medium"


# lmsys-chat-1m (English) okazaki lab
INPUT_DIR=/groups/gag51395/datasets/instruct/lmsys-chat-1m/sft
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt-en.jsonl

mkdir -p $(dirname $OUTPUT_PATH)

python tools/swallow_datasets/qwen3-swallow-instruct/lmsys-chat-1m-convert.py \
  --input-jsonl $INPUT_DIR/lmsys-chat-1m_synthesized_single-turn_conversation_gpt-oss-medium_sft-wo-pii-and-template-instructions-wo-non-toxic-refusal_English.jsonl \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI." \
  --reasoning-effort "medium"

##################################################################

# no thinking trajectory dataset

# code
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-code-deepseek-r1-no-thinking-trajectory.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain-no-think.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B"

# math
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-deepseek-r1-no-thinking-trajectory.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain-no-think.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B"

# science
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science/pretrain/nemotron-post-training-v1-science-deepseek-r1-no-thinking-trajectory.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain-no-think.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B"

# lmsys-chat-1m
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/swallow-sft-reasoning/chat-raw
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-no-thinking-trajectory.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain-no-think.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B"

##################################################################

# Japanese code
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/code/gpt-oss-120b/medium
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-ja-code-gpt-oss-model-identity-chat-gpt.jsonl
python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

# Total invalid records skipped: 84230

# Japanese math
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/math/gpt-oss-120b/medium
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-ja-math-gpt-oss-model-identity-chat-gpt.jsonl
python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."
# Total invalid records skipped: 10925

# Japanese science
INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/science/gpt-oss-120b/medium
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science/pretrain/nemotron-post-training-v1-ja-science-gpt-oss-model-identity-chat-gpt.jsonl
python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "medium" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."

# Total invalid records skipped: 2764

# Nemotron Post Training Code (gpt-oss) reasoning-effort: high

INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/code-jsonl/gpt-oss-120b/high
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-code-gpt-oss-model-identity-chat-gpt-reasoning-effort-high.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "high" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."


# Nemotron Post Training Math (gpt-oss) reasoning-effort: high

INPUT_DIR=/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v1/math-jsonl/gpt-oss-120b/high
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt-reasoning-effort-high.jsonl
python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-pretrain.py \
  --input-dir $INPUT_DIR \
  --output-jsonl $OUTPUT_PATH \
  --input-target-key "conversation" \
  --qwen3-tokenizer "Qwen/Qwen3-235B-A22B" \
  --gpt-oss-tokenizer "openai/gpt-oss-120b" \
  --reasoning-effort "high" \
  --model-identity "You are ChatGPT, a large language model trained by OpenAI."
