#!/bin/bash
#PBS -q rt_HF
#PBS -N math_stage1
#PBS -l select=1
#PBS -l walltime=12:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/stage1_math

set -e
cd $PBS_O_WORKDIR

echo "Nodes allocated to this job:"
cat $PBS_NODEFILE

module load cuda/12.6/12.6.1

USER_DIR="/groups/gag51395/fujii"

# environment variables
export TMP="$USER_DIR/tmp"
export TMP_DIR="$USER_DIR/tmp"
export HF_HOME="$USER_DIR/hf_cache"

source .venv/bin/activate

# finemath: https://huggingface.co/datasets/HuggingFaceTB/finemath
INPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/public/finemath/finemath-3plus-jsonl"
OUTPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-1"
mkdir -p $OUTPUT_DIR

export CUDA_VISIBLE_DEVICES=0
export TOKENIZERS_PARALLELISM="false"

PWD=$(pwd)
export PYTHONPATH=$PWD:$PYTHONPATH
python pipelines/swallow_math/src/content_length_filter.py \
  --input-dir $INPUT_DIR \
  --output-dir $OUTPUT_DIR \
  --tokenizer "/groups/gag51395/hf_checkpoints/Qwen3-32B-FP8"
