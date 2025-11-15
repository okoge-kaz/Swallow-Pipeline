#!/bin/bash

source .venv/bin/activate

# Nemotron-Post-Training-v1 code
INPUT_JSONL=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/code/pretrain/nemotron-post-training-v1-code-gpt-oss-model-identity-chat-gpt.jsonl
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/code/nemotron-post-training-v1-code.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-translate/extract_user_turn.py \
    --input-jsonl $INPUT_JSONL \
    --output-jsonl $OUTPUT_PATH

# Nemotron-Post-Training-v1 math
INPUT_JSONL=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt.jsonl
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/math/nemotron-post-training-v1-math.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-translate/extract_user_turn.py \
    --input-jsonl $INPUT_JSONL \
    --output-jsonl $OUTPUT_PATH


# Nemotron-Post-Training-v1 science
INPUT_JSONL=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1/science/pretrain/nemotron-post-training-v1-science-gpt-oss-model-identity-chat-gpt.jsonl
OUTPUT_PATH=/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/science/nemotron-post-training-v1-science.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/nemotron-post-training-translate/extract_user_turn.py \
    --input-jsonl $INPUT_JSONL \
    --output-jsonl $OUTPUT_PATH
