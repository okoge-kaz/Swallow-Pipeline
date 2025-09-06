#!/bin/bash
#PBS -q rt_HC
#PBS -N convert
#PBS -l select=1:ncpus=32
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/convert_parquet_to_jsonl

set -e
cd $PBS_O_WORKDIR

# environment variables
USER_DIR=/groups/gag51395/fujii

export TMP="$USER_DIR/tmp"
export TMP_DIR="$USER_DIR/tmp"
export HF_HOME="$USER_DIR/hf_cache"

PARQUET_FILE_DIR="/groups/gch51639/fujii/datasets/raw/instruct/public/Nemotron-Post-Training-Dataset-v2/data"
JSONL_FILE_DIR="$PARQUET_FILE_DIR-jsonl"
mkdir -p "${JSONL_FILE_DIR}"

# Convert Parquet files to JSONL
for PARQUET_FILE in "${PARQUET_FILE_DIR}"/*.parquet; do
    BASENAME=$(basename "${PARQUET_FILE}" .parquet)
    JSONL_FILE="${JSONL_FILE_DIR}/${BASENAME}.jsonl"

    echo "Converting ${PARQUET_FILE} to ${JSONL_FILE}"

    python tools/converter/parquet_to_jsonl.py \
        --parquet-file "${PARQUET_FILE}" \
        --jsonl-file "${JSONL_FILE}"
    echo "Conversion completed: ${JSONL_FILE}"
    echo "----------------------------------------"
done
