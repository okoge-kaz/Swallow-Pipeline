#!/bin/bash

source .venv/bin/activate

# code
python tools/swallow_datasets/qwen3-swallow-instruct/merge_translated.py \
  --input-dir /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/code/gpt-oss-120b/medium/ \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/code/nemotron-post-training-user-turn.jsonl \
  --input-target-key conversation

# Total: 1888684
# Kept: 1885456
# empty_count: 51
# over_refusal_count: 2389
# invalid_count: 788

# math
python tools/swallow_datasets/qwen3-swallow-instruct/merge_translated.py \
  --input-dir /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/math/gpt-oss-120b/medium/ \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/math/nemotron-post-training-user-turn.jsonl \
  --input-target-key conversation

# Total: 2035007
# Kept: 2024431
# empty_count: 302
# over_refusal_count: 8989
# invalid_count: 1285

# science
python tools/swallow_datasets/qwen3-swallow-instruct/merge_translated.py \
  --input-dir /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/translated-nemotron-post-training-v1/science/gpt-oss-120b/medium/ \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/nemotron-post-training-v1-ja/science/nemotron-post-training-user-turn.jsonl \
  --input-target-key conversation

# Total: 2486130
# Kept: 2484364
# empty_count: 121
# over_refusal_count: 865
# invalid_count: 780
