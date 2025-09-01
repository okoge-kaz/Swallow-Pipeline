#!/bin/bash
#PBS -q rt_HC
#PBS -N nemotron-cc-hq-actual
#PBS -l select=1:ncpus=32
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/nemotron-cc

set -e
cd $PBS_O_WORKDIR

# https://data.commoncrawl.org/contrib/Nemotron/Nemotron-CC/data-jsonl.paths.gz
INPUT_FILE="/groups/gag51395/datasets/raw/pretrain/nemotron-cc/data-jsonl.paths"
BASE_URL="https://data.commoncrawl.org/"
OUTPUT_DIR="/groups/gag51395/datasets/raw/pretrain/nemotron-cc/downloads"
MERGED_DIR="/groups/gag51395/datasets/raw/pretrain/nemotron-cc/merged"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$MERGED_DIR"

# get paths with quality=high/kind=actual (= Nemotron-CC-HQ-Actual)
FILTERED_PATHS=$(grep "quality=high/kind=actual" "$INPUT_FILE")

if [ -z "$FILTERED_PATHS" ]; then
    echo "No paths matching 'quality=high/kind=actual' found."
    exit 1
fi

echo "$FILTERED_PATHS" | while IFS= read -r path; do
    if [ -z "$path" ]; then continue; fi

    filename=$(basename "$path")
    url="${BASE_URL}${path}"
    zstd_file="${OUTPUT_DIR}/${filename}"
    jsonl_file="${OUTPUT_DIR}/${filename%.zstd}"

    # download with retry on 503 errors
    if ! wget --tries=3 --retry-on-http-error=503 -O "$zstd_file" "$url"; then
        echo "Failed to download: $url"
        continue
    fi

    # decompress
    if ! zstd -d -f "$zstd_file" -o "$jsonl_file"; then
        echo "Failed to decompress: $zstd_file"
        continue
    fi

    # extract year (ex: CC-MAIN-2024-30-part-00083.jsonl → 2024)
    year=$(echo "$filename" | sed -n 's/.*CC-MAIN-\([0-9]\{4\}\)-.*/\1/p')
    if [ -z "$year" ]; then
        echo "Could not extract year from: $filename"
        continue
    fi

    # append to merged file for that year
    merged_file="${MERGED_DIR}/merged_${year}.jsonl"
    cat "$jsonl_file" >> "$merged_file"
    if [ $? -eq 0 ]; then
        echo "Merged $jsonl_file into $merged_file"
    else
        echo "Failed to merge: $jsonl_file"
    fi

done

echo "Processing completed."
