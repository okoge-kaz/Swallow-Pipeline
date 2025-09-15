#!/bin/bash
#PBS -q rt_HG
#PBS -N translate
#PBS -l select=1
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/translate

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

INPUT_FILE_PATH=$SWALLOW_CODE_DIR/qa/python/medium_quality/Qwen3-30B-A3B-Instruct-2507-FP8/train_$INDEX.jsonl
OUTPUT_FILE_PATH=$SWALLOW_CODE_DIR/qa/python/medium_quality/Qwen3-30B-A3B-Instruct-2507-FP8/translated_japanese/train_$INDEX.jsonl
mkdir -p $(dirname $OUTPUT_FILE_PATH)

export TOKENIZERS_PARALLELISM="false"
export PYTHONPATH="/groups/gag51395/fujii/src/swallow-code-v2:$PYTHONPATH"
export CUDA_VISIBLE_DEVICES="0"

PWD=$(pwd)
export PYTHONPATH=$PWD:$PYTHONPATH

python pipelines/swallow_code/accepted/translate.py \
  --model-path /groups/gag51395/hf_checkpoints/$MODEL_NAME \
  --input-jsonl "$INPUT_FILE_PATH" \
  --output-jsonl "$OUTPUT_FILE_PATH" \
  --gen-max-tokens 65536 \
  --batch-size 4096 \
  --tensor-parallel-size 1
