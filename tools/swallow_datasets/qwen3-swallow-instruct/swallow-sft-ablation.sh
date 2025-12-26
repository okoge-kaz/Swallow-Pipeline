#!/bin/bash

source .venv/bin/activate

NEMOTRON_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/nemotron-post-training-v1"
SWALLOW_DIR="/groups/gch51639/fujii/datasets/raw/instruct/swallow/sft-ablation"

# Exp1 (DeepSeek R1 0528)
head -n 200000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp1/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp1/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp1/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp1/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp1/train.jsonl

# Exp2 (GPT_OSS-120B)
head -n 200000 ${NEMOTRON_DIR}/code/pretrain/nemotron-post-training-v1-code-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp2/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp2/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/pretrain/nemotron-post-training-v1-science-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp2/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp2/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp2/train.jsonl

# Exp3 (DeepSeek R1 0528 Japanese)
NEMOTRON_JA_DIR="/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/swallow-sft-reasoning"
head -n 200000 ${NEMOTRON_JA_DIR}/code/nemotron-post-training-v1-code-ja-32k-200k.jsonl >> ${SWALLOW_DIR}/exp3/merged.jsonl
head -n 200000 ${NEMOTRON_JA_DIR}/math/nemotron-post-training-v1-math-ja-32k-200k.jsonl >> ${SWALLOW_DIR}/exp3/merged.jsonl
head -n 100000 ${NEMOTRON_JA_DIR}/stem/nemotron-post-training-v1-stem-ja-32k-100k.jsonl >> ${SWALLOW_DIR}/exp3/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp3/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp3/train.jsonl

# Exp4 (GPT-OSS-120B Japanese)
head -n 200000 ${NEMOTRON_DIR}/code/pretrain/nemotron-post-training-v1-ja-code-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp4/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/pretrain/nemotron-post-training-v1-ja-math-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp4/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/pretrain/nemotron-post-training-v1-ja-science-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp4/merged.jsonl
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp4/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp4/train.jsonl

# Exp5 (DeepSeek R1 0528 + Scaling)
head -n 600000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp5/merged.jsonl
head -n 600000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp5/merged.jsonl
head -n 300000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp5/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp5/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp5/train.jsonl

# Exp6 (DeepSeek R1 0528 + LMSYS-JA)
head -n 200000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp6/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp6/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp6/merged.jsonl
head -n 100000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp6/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp6/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp6/train.jsonl

# Exp7 (DeepSeek R1 0528 + LMSYS-En)
head -n 200000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp7/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp7/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp7/merged.jsonl
head -n 100000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt-en.jsonl >> ${SWALLOW_DIR}/exp7/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp7/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp7/train.jsonl

# Exp8 (DeepSeek R1 0528 + GPT-OSS-Japanese)
head -n 100000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 50000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/code/pretrain/nemotron-post-training-v1-ja-code-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/math/pretrain/nemotron-post-training-v1-ja-math-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 50000 ${NEMOTRON_DIR}/science/pretrain/nemotron-post-training-v1-ja-science-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 50000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl
head -n 50000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt-en.jsonl >> ${SWALLOW_DIR}/exp8/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp8/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp8/train.jsonl

# Exp9 (no thinking lmsys Japanese)
head -n 200000 ${NEMOTRON_DIR}/code/nemotron-post-training-v1-code-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp9/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/nemotron-post-training-v1-math-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp9/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/nemotron-post-training-v1-science-deepseek-r1.jsonl >> ${SWALLOW_DIR}/exp9/merged.jsonl
head -n 100000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-no-thinking-trajectory.jsonl >> ${SWALLOW_DIR}/exp9/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp9/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp9/train.jsonl

# Exp10
head -n 50000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt.jsonl >> ${SWALLOW_DIR}/exp10/merged.jsonl
head -n 50000 /groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-reasoning/lmsys-chat-1m/pretrain/lmsys-chat-1m-okazaki-lab-gpt-oss-model-identity-chat-gpt-en.jsonl >> ${SWALLOW_DIR}/exp10/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp10/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp10/train.jsonl

# Exp11
head -n 200000 ${NEMOTRON_DIR}/code/pretrain/nemotron-post-training-v1-code-gpt-oss-model-identity-chat-gpt-reasoning-effort-high.jsonl >> ${SWALLOW_DIR}/exp11/merged.jsonl
head -n 200000 ${NEMOTRON_DIR}/math/pretrain/nemotron-post-training-v1-math-gpt-oss-model-identity-chat-gpt-reasoning-effort-high.jsonl >> ${SWALLOW_DIR}/exp11/merged.jsonl
head -n 100000 ${NEMOTRON_DIR}/science/pretrain/nemotron-post-training-v1-science-gpt-oss-model-identity-chat-gpt-reasoning-effort-high.jsonl >> ${SWALLOW_DIR}/exp11/merged.jsonl

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/filter.py \
  --input-jsonl ${SWALLOW_DIR}/exp11/merged.jsonl \
  --output-jsonl ${SWALLOW_DIR}/exp11/train.jsonl
