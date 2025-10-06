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

source .ven/bin/activate

export TMP=/local/$PBS_JOBID
export TMPDIR=$TMP

DATASET_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/public/Nemotron-Pretraining-Code-v1

python tools/public_datasets/nemotron-pretraining-code-v1/split_by_language.py \
  --input-dir $DATASET_DIR/Nemotron-Code-Metadata \
  --output-dir $DATASET_DIR/Nemotron-Code-Metadata-split \
  --rows-per-file 1000000 \
  --batch-size 100000 \
  --compression snappy
