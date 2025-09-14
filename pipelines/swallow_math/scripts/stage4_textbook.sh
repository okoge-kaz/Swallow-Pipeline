#!/bin/bash
#PBS -q rt_HF
#PBS -N math_textbook_style
#PBS -l select=1
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -m n
#PBS -v USE_SSH=1
#PBS -koed
#PBS -V
#PBS -o outputs/pipeline/math/textbook_style

set -e
cd "$PBS_O_WORKDIR"

echo "Nodes allocated to this job:"
cat "$PBS_NODEFILE"

# Check INDEX
if [ -z "${INDEX:-}" ]; then
  echo "Error: INDEX variable is not set"
  exit 1
fi

# Keep numeric before padding
INDEX_INT=$((10#$INDEX))  # tolerate leading zeros
if [ "$INDEX_INT" -lt 0 ] || [ "$INDEX_INT" -gt 127 ]; then
  echo "Error: INDEX must be in [0,127], got $INDEX_INT"
  exit 1
fi
OTHER_INT=$((127 - INDEX_INT))

# Zero-pad to 5 digits
INDEX_PAD=$(printf "%05d" "$INDEX_INT")
OTHER_PAD=$(printf "%05d" "$OTHER_INT")

module load cuda/12.6/12.6.1
USER_DIR="/groups/gag51395/fujii"

# environment variables
export TMP="$USER_DIR/tmp"
export TMP_DIR="$USER_DIR/tmp"
export HF_HOME="$USER_DIR/hf_cache"

source .venv/bin/activate

INPUT_DIR=/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-3
INPUT_A="$INPUT_DIR/train-${INDEX_PAD}-Qwen3-32B-FP8.jsonl"
INPUT_B="$INPUT_DIR/train-${OTHER_PAD}-Qwen3-32B-FP8.jsonl"

OUTPUT_DIR="/groups/gch51639/fujii/datasets/raw/pretrain/swallow/swallow-math-v2/stage-4-textbook"
mkdir -p "$OUTPUT_DIR"

MODEL_NAME=Qwen3-235B-A22B-Thinking-2507-FP8

export TOKENIZERS_PARALLELISM="false"
PWD=$(pwd)
export PYTHONPATH=$PWD:$PYTHONPATH

# --- shard A: INDEX (GPU 0-3) ---
export CUDA_VISIBLE_DEVICES=0,1,2,3
python pipelines/swallow_math/src/run.py math_rewrite \
  --input-jsonl "$INPUT_A" \
  --output-jsonl "$OUTPUT_DIR/train-${INDEX_PAD}-${MODEL_NAME}.jsonl" \
  --model "/groups/gag51395/hf_checkpoints/${MODEL_NAME}" \
  --batch-size 4096 \
  --tensor-parallel-size 4 \
  --input-jsonl-key "text" \
  --llm-output-jsonl-key "llm_output" \
  --math-text-jsonl-key "llm_extracted_math_text" \
  --prompt-type "text-book-style" &

PID_A=$!

# --- shard B: 127-INDEX (GPU 4-7) ---
export CUDA_VISIBLE_DEVICES=4,5,6,7
python pipelines/swallow_math/src/run.py math_rewrite \
  --input-jsonl "$INPUT_B" \
  --output-jsonl "$OUTPUT_DIR/train-${OTHER_PAD}-${MODEL_NAME}.jsonl" \
  --model "/groups/gag51395/hf_checkpoints/${MODEL_NAME}" \
  --batch-size 4096 \
  --tensor-parallel-size 4 \
  --input-jsonl-key "text" \
  --llm-output-jsonl-key "llm_output" \
  --math-text-jsonl-key "llm_extracted_math_text" \
  --prompt-type "text-book-style" &

PID_B=$!

# Wait both (propagate failures)
set +e
wait "$PID_A"; S1=$?
wait "$PID_B"; S2=$?
set -e

if [ $S1 -ne 0 ] || [ $S2 -ne 0 ]; then
  echo "Error: one of the parallel runs failed (A=$S1, B=$S2)"
  exit 1
fi

echo "Done:"
echo " - $OUTPUT_DIR/train-${INDEX_PAD}-${MODEL_NAME}.jsonl"
echo " - $OUTPUT_DIR/train-${OTHER_PAD}-${MODEL_NAME}.jsonl"
