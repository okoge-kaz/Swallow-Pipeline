#!/bin/bash

# save OpenCodeReasoning-2 with questions
OPEN_CODE_REASONING_2_DIR="/groups/gag51395/datasets/raw/instruct/OpenCodeReasoning-2/"

python tools/public_datasets/open_code_reasoning_2/build.py \
  --output-dir $OPEN_CODE_REASONING_2_DIR/jsonl \
  --format jsonl

# convert into pre-training format

# Python
python tools/public_datasets/open_code_reasoning_2/run.py \
  --input-jsonl $OPEN_CODE_REASONING_2_DIR/jsonl/ocr2_python_with_questions.jsonl \
  --output-jsonl $OPEN_CODE_REASONING_2_DIR/pretrain/open_code_reasoning_2_r1_generation_python.jsonl \
  --mode r1_generation

python tools/public_datasets/open_code_reasoning_2/run.py \
  --input-jsonl $OPEN_CODE_REASONING_2_DIR/jsonl/ocr2_python_with_questions.jsonl \
  --output-jsonl $OPEN_CODE_REASONING_2_DIR/pretrain/open_code_reasoning_2_solution_python.jsonl \
  --mode solution

# C++
python tools/public_datasets/open_code_reasoning_2/run.py \
  --input-jsonl $OPEN_CODE_REASONING_2_DIR/jsonl/ocr2_cpp_with_questions.jsonl \
  --output-jsonl $OPEN_CODE_REASONING_2_DIR/pretrain/open_code_reasoning_2_r1_generation_cpp.jsonl \
  --mode r1_generation

python tools/public_datasets/open_code_reasoning_2/run.py \
  --input-jsonl $OPEN_CODE_REASONING_2_DIR/jsonl/ocr2_cpp_with_questions.jsonl \
  --output-jsonl $OPEN_CODE_REASONING_2_DIR/pretrain/open_code_reasoning_2_solution_cpp.jsonl \
  --mode solution
