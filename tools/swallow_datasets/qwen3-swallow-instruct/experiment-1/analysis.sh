#!/bin/sh
#PBS -q rt_HC
#PBS -N analysis
#PBS -l select=1:ncpus=32
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m n
#PBS -koed
#PBS -V
#PBS -o outputs/swallow_datasets/qwen3-swallow-instruct/

cd $PBS_O_WORKDIR

SCRIPT_DIR=/groups/gag51395/fujii/src/Swallow-Pipeline
cd $SCRIPT_DIR

source .venv/bin/activate

DATASET_DIR="/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1"
FIGURE_DIR=$SCRIPT_DIR/figures/swallow-post-training/qwen3-swallow-instruct/experiment-1
mkdir -p $FIGURE_DIR

# Nemotron Post Training v1 Math
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v1-math.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v1-math-token-length.png

# Nemotron Post Training v1 STEM
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v1-stem.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v1-stem-token-length.png

# Nemotron Post Training v1 Code
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v1-code.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v1-code-token-length.png

# Nemotron Post Training v2 Math
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v2-math.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v2-math-token-length.png

# Nemotron Post Training v2 STEM
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v2-stem.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v2-stem-token-length.png

# Nemotron Post Training v2 Code
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v2-code.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v2-code-token-length.png
