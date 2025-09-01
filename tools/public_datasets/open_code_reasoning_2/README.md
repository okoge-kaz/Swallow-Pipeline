# OpenCodeReasoning-2 Dataset Processing Tools

This directory contains tools for processing the [OpenCodeReasoning-2 dataset](https://huggingface.co/datasets/nvidia/OpenCodeReasoning-2) for LLM pre-training. The dataset requires a two-step processing pipeline to handle missing question fields and convert to training format.

## Overview

The OpenCodeReasoning-2 dataset has missing `question` field values (marked as "-"). This processing pipeline:

1. **build.py**: Retrieves and combines question fields from source datasets to create valid data
2. **run.py**: Converts the data to pre-training format including the thinking process

## Processing Pipeline

### Step 1: Question Field Reconstruction (build.py)

The `build.py` script addresses the missing question fields by:
- Loading source datasets (TACO, APPS, CodeContests, Codeforces)
- Mapping dataset references to retrieve actual question content
- Combining question fields to create complete, valid dataset entries

**Usage:**
```bash
python build.py --output-dir <output_directory> --format jsonl
```

**Parameters:**
- `--output-dir`: Directory to save processed files
- `--format`: Output format (`jsonl` or `json`, default: `jsonl`)

### Step 2: Pre-training Format Conversion (run.py)

The `run.py` script converts the data to pre-training format by:
- Filtering entries where `judgement == "right"`
- Combining question and reasoning process (`r1_generation`) into training text
- Creating structured format: "Question:\n\n{question}\n\nSolution:\n\n{r1_generation}"

**Usage:**
```bash
python run.py --input-jsonl <input_file.jsonl> --output-jsonl <output_file.jsonl>
```

**Parameters:**
- `--input-jsonl`: Input JSONL file (output from build.py)
- `--output-jsonl`: Output JSONL file for pre-training

## Complete Workflow

```bash
# Step 1: Reconstruct missing question fields
python build.py --output-dir ./processed --format jsonl

# Step 2: Convert to pre-training format (for each language)
python run.py \
  --input-jsonl ./processed/ocr2_python_with_questions.jsonl \
  --output-jsonl ./processed/ocr2_python_pretrain.jsonl

python run.py \
  --input-jsonl ./processed/ocr2_cpp_with_questions.jsonl \
  --output-jsonl ./processed/ocr2_cpp_pretrain.jsonl
```

## Output Format

The final pre-training data includes:
- Original dataset fields
- `text` field containing formatted question and solution for training
- Only entries with correct judgements (`judgement == "right"`)
