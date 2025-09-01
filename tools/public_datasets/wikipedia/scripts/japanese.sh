#!/bin/bash
#PBS -q rt_HC
#PBS -N stage1
#PBS -l select=1:ncpus=32
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/wikipedia

set -e
cd $PBS_O_WORKDIR

source .venv/bin/activate

DATASET_HOME_DIR=/groups/gag51395/datasets/raw/pretrain
WIKIPEDIA_DIR=${DATASET_HOME_DIR}/wikipedia/raw
PROCESSED_DIR=${DATASET_HOME_DIR}/wikipedia/processed
mkdir -p $WIKIPEDIA_DIR
mkdir -p $PROCESSED_DIR

# 1. Download wikipedia dump
if [ ! -f $WIKIPEDIA_DIR/ja_wiki.json.tar.gz ]; then
  wget -c https://dumps.wikimedia.org/other/enterprise_html/runs/20250320/jawiki-NS0-20250320-ENTERPRISE-HTML.json.tar.gz -O $WIKIPEDIA_DIR/ja_wiki.json.tar.gz
fi

# 2. Extract
if [ ! -d $WIKIPEDIA_DIR/ja_wiki ]; then
  mkdir -p $WIKIPEDIA_DIR/ja_wiki
  tar -xvzf $WIKIPEDIA_DIR/ja_wiki.json.tar.gz -C $WIKIPEDIA_DIR/ja_wiki
fi

# 3. Process
python tools/public_datasets/wikipedia/japanese/run.py \
  --input-dir $WIKIPEDIA_DIR/ja_wiki \
  --output-file $PROCESSED_DIR/ja_wikipedia.jsonl
