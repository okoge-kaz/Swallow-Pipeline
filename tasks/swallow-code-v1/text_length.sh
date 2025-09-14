#!/bin/bash
#PBS -q rt_HC
#PBS -N analysis
#PBS -l select=1:ncpus=32
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/analysis

set -e
cd $PBS_O_WORKDIR

USER_DIR="/groups/gag51395/fujii"

# environment variables
export TMP="$USER_DIR/tmp"
export TMP_DIR="$USER_DIR/tmp"
export HF_HOME="$USER_DIR/hf_cache"

source .venv/bin/activate

SWALLOW_CODE_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-code-v1

# EXP3
echo "EXP 3: linter filtering"
python tasks/swallow-code-v1/text_length.py \
  --input-dir $SWALLOW_CODE_DIR/ablation/exp3-linter-filtered/jsonl \
  --analysis-key "text" \

# EXP5: SGCR
echo "EXP 5: SGCR"
python tasks/swallow-code-v1/text_length.py \
  --input-dir $SWALLOW_CODE_DIR/ablation/exp5-sgcr/jsonl \
  --analysis-key "text"

# EXP11 SCOR
echo "EXP 11: SCOR"
python tasks/swallow-code-v1/text_length.py \
  --input-dir $SWALLOW_CODE_DIR/ablation/exp11-scor/jsonl \
  --analysis-key "text"
