#!/bin/bash
#PBS -q rt_HG
#PBS -N math_stage4
#PBS -l select=1
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/stage4_planning

set -e
cd $PBS_O_WORKDIR

echo "Nodes allocated to this job:"
cat $PBS_NODEFILE

# Check if INDEX is provided
if [ -z "$INDEX" ]; then
  echo "Error: INDEX variable is not set"
  exit 1
fi

module load cuda/12.6/12.6.1
INDEX=$(printf "%05d" $INDEX)
USER_DIR="/groups/gag51395/fujii"

# environment variables
export TMP="$USER_DIR/tmp"
export TMP_DIR="$USER_DIR/tmp"
export HF_HOME="$USER_DIR/hf_cache"

source .venv/bin/activate

MODEL_NAME=Qwen3-30B-A3B-Thinking-2507-FP8

INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-3
INPUT_FILE_PATH="$INPUT_DIR/train-${INDEX}-Qwen3-32B-FP8.jsonl"
OUTPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-4-ablations/planning/${MODEL_NAME}"
mkdir -p $OUTPUT_DIR

export CUDA_VISIBLE_DEVICES=0
export TOKENIZERS_PARALLELISM="false"
PWD=$(pwd)
export PYTHONPATH=$PWD:$PYTHONPATH

python pipelines/swallow_math/src/run.py math_rewrite \
  --input-jsonl $INPUT_FILE_PATH \
  --output-jsonl $OUTPUT_DIR/train-${INDEX}.jsonl \
  --model "/groups/gag51395/hf_checkpoints/${MODEL_NAME}" \
  --batch-size 4096 \
  --tensor-parallel-size 1 \
  --prompt-type "planning-approach" \
  --input-jsonl-key "text" \
  --llm-output-jsonl-key "llm_output" \
  --math-text-jsonl-key "llm_extracted_math_text"
