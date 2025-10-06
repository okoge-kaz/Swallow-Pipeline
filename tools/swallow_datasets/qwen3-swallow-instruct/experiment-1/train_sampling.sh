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

# Nemotron Post Training v2 Code <=32k 20k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-code.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-code-32k-20k.jsonl \
  --max-tokens 32768 \
  --num-samples 20000

# Nemotron Post Training v2 Math <=32k 20k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-math.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-math-32k-20k.jsonl \
  --max-tokens 32768 \
  --num-samples 20000

# Nemotron Post Training v2 STEM <=32k 10k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-stem.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-stem-32k-10k.jsonl \
  --max-tokens 32768 \
  --num-samples 10000

# Nemotron Post Training v2 STEM <=32k 36k
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-stem.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v2-stem-32k-36k.jsonl \
  --max-tokens 32768 \
  --num-samples 36000

# Nemotron Post Training v1 Code <= 32k 200k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-code-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-code-ja-32k-200k.jsonl \
  --max-tokens 32768 \
  --num-samples 200000

# Nemotron Post Training v1 Math <= 32k 200k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-math-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-math-ja-32k-200k.jsonl \
  --max-tokens 32768 \
  --num-samples 200000

# Nemotron Post Training v1 STEM <= 32k 100k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-stem-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-stem-ja-32k-100k.jsonl \
  --max-tokens 32768 \
  --num-samples 100000


# Nemotron Post Training v1 Code <= 32k 20k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-code-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-code-ja-32k-20k.jsonl \
  --max-tokens 32768 \
  --num-samples 20000

# Nemotron Post Training v1 Math <= 32k 20k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-math-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-math-ja-32k-20k.jsonl \
  --max-tokens 32768 \
  --num-samples 20000

# Nemotron Post Training v1 STEM <= 32k 10k (Japanese)
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/train_sampling.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-stem-ja.jsonl \
  --output-json /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp4/nemotron-post-training-v1-stem-ja-32k-10k.jsonl \
  --max-tokens 32768 \
  --num-samples 10000
