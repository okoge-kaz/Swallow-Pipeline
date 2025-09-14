#!/bin/bash
#PBS -q rt_HG
#PBS -N code_question
#PBS -l select=1
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/swallow-code-v2/qa

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
MODEL_NAME=Qwen3-30B-A3B-Instruct-2507-FP8

INDEX=60
INDEX=$(printf "%04d" $INDEX)

SWALLOW_CODE_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-code-v2

INPUT_FILE_PATH=$SWALLOW_CODE_DIR/stage5-auto-format/python/medium_quality/Qwen3-235B-A22B-Instruct-2507-FP8/train_$INDEX.jsonl
OUTPUT_FILE_PATH=$SWALLOW_CODE_DIR/qa/python/medium_quality/Qwen3-30B-A3B-Instruct-2507-FP8/train_$INDEX.jsonl

export TOKENIZERS_PARALLELISM="false"
export CUDA_VISIBLE_DEVICES="0"

PWD=$(pwd)
export PYTHONPATH=$PWD:$PYTHONPATH

python pipelines/swallow_code/accepted/qa.py \
  --model-path /groups/gag51395/hf_checkpoints/$MODEL_NAME \
  --input-jsonl "$INPUT_FILE_PATH" \
  --output-jsonl "$OUTPUT_FILE_PATH" \
  --gen-max-tokens 8192 \
  --batch-size 1000 \
  --tensor-parallel-size 1
