#!/bin/sh
#PBS -q rt_HF
#PBS -N deduplicate
#PBS -l select=1:ncpus=192
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m n
#PBS -koed
#PBS -V
#PBS -o outputs/swallow_datasets/qwen3-swallow-instruct/

cd $PBS_O_WORKDIR

SCRIPT_DIR=/groups/gag51395/fujii/src/Swallow-Pipeline

cd ${SCRIPT_DIR}
source .venv/bin/activate

# Nemotron Post Training v1 STEM deduplication
python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/nemotron_post_training_deduplicate.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-stem.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/nemotron-post-training-v1-stem-deduplicated.jsonl

# Nemotron Post Training v1 STEM token length plot
DATASET_DIR="/groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1"
FIGURE_DIR=$SCRIPT_DIR/figures/swallow-post-training/qwen3-swallow-instruct/experiment-1

python tools/swallow_datasets/qwen3-swallow-instruct/experiment-1/token_length.py \
  --input-jsonl $DATASET_DIR/nemotron-post-training-v1-stem-deduplicated.jsonl \
  --tokenizer-path /groups/gag51395/hf_checkpoints/Qwen3-8B \
  --plot-path $FIGURE_DIR/nemotron-post-training-v1-stem-token-length.png
