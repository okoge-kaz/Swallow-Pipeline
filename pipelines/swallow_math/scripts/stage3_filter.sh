#!/bin/bash
#PBS -q rt_HF
#PBS -N math_stage3
#PBS -l select=1
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/stage3_math

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

INPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-2"
OUTPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-3"
mkdir -p $OUTPUT_DIR

python pipelines/swallow_math/src/filter.py \
  --input-dir $INPUT_DIR \
  --output-dir $OUTPUT_DIR \
  --filter-target-jsonl-key "llm_extracted_math_text"
