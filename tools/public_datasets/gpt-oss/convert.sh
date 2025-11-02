#!/bin/bash

# open math reasoning
python tools/public_datasets/gpt-oss/convert_gpt_oss_style.py \
  --input-jsonl /groups/gag51395/datasets/raw/instruct/OpenMathReasoning/pretrain.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-math-reasoning/instruct.jsonl \
  --question-key problem \
  --answer-key generated_solution \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open code reasoning (python)
python tools/public_datasets/gpt-oss/convert_gpt_oss_style.py \
  --input-jsonl /groups/gag51395/datasets/raw/instruct/OpenCodeReasoning-2/jsonl/ocr2_python_with_questions.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-code-reasoning-2/python_instruct.jsonl \
  --question-key question \
  --answer-key r1_generation \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open code reasoning (cpp)
python tools/public_datasets/gpt-oss/convert_gpt_oss_style.py \
  --input-jsonl /groups/gag51395/datasets/raw/instruct/OpenCodeReasoning-2/jsonl/ocr2_cpp_with_questions.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-code-reasoning-2/cpp_instruct.jsonl \
  --question-key question \
  --answer-key r1_generation \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open science reasoning
python tools/public_datasets/gpt-oss/convert_gpt_oss_style.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/public/OpenScienceReasoning-2/train-jsonl/train_open_science_reasoning_2_r1_generation.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-science-reasoning-2/instruct.jsonl \
  --question-key question \
  --answer-key r1_generation \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open code reasoning text section (python)
python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-code-reasoning-2/python_instruct.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open code reasoning text section (cpp)
python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-code-reasoning-2/cpp_instruct.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open science reasoning text section
python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-science-reasoning-2/instruct.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# open math reasoning text section
python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/open-math-reasoning/instruct.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# lmsys chat 1m (ja)
python tools/public_datasets/gpt-oss/lmsys-chat-1m-gpt-oss.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/lmsys-chat-1m-gpt-oss-ja_delete-repetition.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-ja_delete-repetition.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# lmsys chat 1m (en)
python tools/public_datasets/gpt-oss/lmsys-chat-1m-gpt-oss.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/instruct/swallow/Qwen3-Swallow-SFT/exp1/lmsys-chat-1m-gpt-oss-en_delete-repetition.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-en_delete-repetition.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

# remove gpt-oss-tag
python tools/public_datasets/gpt-oss/delete_tag.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-ja_delete-repetition.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-ja-train.jsonl \
  --remove

python tools/public_datasets/gpt-oss/delete_tag.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-en_delete-repetition.jsonl \
  --output-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-en-train.jsonl \
  --remove

# lmsys chat 1m (text)
python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-ja-train.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b

python tools/public_datasets/gpt-oss/add_text.py \
  --input-jsonl /groups/gch51639/fujii/datasets/raw/pretrain/public/gpt-oss-reasoning/general-chat/lmsys-chat-1m-gpt-oss-en-train.jsonl \
  --tokenizer-dir /groups/gag51395/hf_checkpoints/gpt-oss-20b
