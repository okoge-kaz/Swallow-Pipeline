#!/bin/bash


# download OpenMathReasoning dataset from Hugging Face
DATASET_DOWNLOAD_DIR="/groups/gag51395/datasets/raw/instruct"
cd $DATASET_DOWNLOAD_DIR

git clone https://huggingface.co/datasets/nvidia/OpenMathReasoning

# convert parquet to jsonl
qsub tools/converter/parquet_to_jsonl.sh  # please change the script

# convert jsonl into the format for pre-training
python tools/public_datasets/open_math_reasoning/run.py \
  --directory $DATASET_DOWNLOAD_DIR/OpenMathReasoning/data-jsonl \
  --output-jsonl $DATASET_DOWNLOAD_DIR/OpenMathReasoning/pretrain.jsonl

