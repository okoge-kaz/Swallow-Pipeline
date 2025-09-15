<div align="center">

# Swallow-Pipeline

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache2.0-green.svg)](LICENSE)

</div>

End-to-end data generation and processing pipelines for training large language models (LLMs). This repository includes reusable components to synthesize instructional content, math-focused texts, and code-related Q&A data using vLLM, along with utilities for dataset preparation.

## Features

- Synthetic content generation with thinking-mode support via vLLM
- Pipelines for educational prose (Cosmopedia), math rewriting, and code Q&A
- JSONL streaming for scalable batch processing
- Utilities for public datasets (Wikipedia, code/math reasoning, multilingual cleaning)
- Ready-to-use evaluation harness integrations (BigCode Bench, LiveCodeBench, EvalPlus, LM Eval)

## Repository Layout

```
pipelines/
  swallow_cosmopedia/   # Educational content and math text generation (vLLM)
  swallow_math/         # Math text rewriting pipeline + scripts
  swallow_code/         # Code Q&A generation and EN -> JA translation
tools/
  public_datasets/      # Converters/cleaners for public datasets
  converter/            # Arrow/Parquet → JSONL converters
  swallow_datasets/     # Dataset-specific tools (e.g., Swallow code v2)
evaluation/             # References for evaluation harnesses
tasks/                  # Task-specific configs or splits
figures/, outputs/      # Artifacts, results (gitignored as appropriate)
pyproject.toml          # Dependencies (Python >= 3.12)
ruff.toml               # Lint/format config
LICENSE                 # Apache-2.0
```

## Requirements

- Python 3.12+
- NVIDIA GPU(s) with recent CUDA drivers for vLLM
- Sufficient GPU memory for your selected model and tensor parallelism

## Installation

The repo is dependency-managed via `pyproject.toml`. The recommended path is to use `uv` for fast, reproducible envs. Alternatively, install core dependencies with pip.

Using uv:

```
uv venv
uv sync
```

Using pip (minimal set):

```
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install bs4 datasets flashinfer-python matplotlib numpy pydantic ruff seaborn tqdm transformers vllm
```

Note: vLLM requires a CUDA-enabled environment. Refer to vLLM docs for GPU/driver compatibility.

## Quick Start

All pipelines read and write JSONL. Inputs are processed in batches and outputs are appended/written line-by-line to avoid memory spikes.

### 1) Educational Content (Cosmopedia)

Generate instructional content from prompts in an input JSONL.

Input JSONL must contain a key `prompt`. The output will add a `generated_text` field plus generation metadata.

```
python pipelines/swallow_cosmopedia/cosmopedia.py \
  --input-jsonl path/to/input.jsonl \
  --output-jsonl path/to/output.jsonl \
  --model Qwen/Qwen3-235B-A22B-Thinking-2507-FP8 \
  --batch-size 32 \
  --tensor-parallel-size 2 \
  --model-max-length 40960 \
  --max-new-tokens 20480
```

Flags: `--enable-thinking` to force enable, `--disable-thinking` to disable (default is enabled).

Keys:
- Input: `prompt`
- Output: `generated_text`

There is also a math-focused variant with a stricter system prompt:

```
python pipelines/swallow_cosmopedia/automath.py \
  --input-jsonl path/to/input.jsonl \
  --output-jsonl path/to/output.jsonl \
  --model Qwen/Qwen3-235B-A22B-Thinking-2507-FP8 \
  --batch-size 32 \
  --tensor-parallel-size 2 \
  --model-max-length 40960 \
  --max-new-tokens 16384
```

### 2) Math Text Rewriting

Rewrites math-related texts into structured forms (e.g., textbook style, Q&A, planning, Socratic, multiple-solution).

Input JSONL must contain a key `text`. The output adds `llm_output` and `math_text` (extracted segment).

```
python pipelines/swallow_math/src/run.py math_rewrite \
  --input-jsonl path/to/input.jsonl \
  --output-jsonl path/to/output.jsonl \
  --model Qwen/Qwen3-235B-A22B-Thinking-2507-FP8 \
  --batch-size 1024 \
  --tensor-parallel-size 2 \
  --model-max-length 40960 \
  --prompt-type pre-train-text
```

Keys:
- Input: `text` (configurable via `--input-jsonl-key`)
- Output: `llm_output`, `math_text`

Prompt types: `pre-train-text`, `text-book-style`, `question-answer`, `planning-approach`, `socratic-method`, `multiple-solution`.

### 3) Code -> Question Generation (English)

Creates an English problem statement that matches a given Python solution.

Input JSONL should provide the code under `improved_code`. Output lines contain `{ "question": ..., "answer": <original code> }`.

```
python pipelines/swallow_code/accepted/qa.py \
  --input-jsonl path/to/code.jsonl \
  --output-jsonl path/to/qa.jsonl \
  --model-path <path-or-HF-ID> \
  --batch-size 4096 \
  --gen-max-tokens 16384 \
  --tensor-parallel-size 1
```

### 4) EN -> JA Translation (Questions and Code Docstrings/Comments)

Translates both the natural language question and the code’s docstrings/comments into Japanese.

Input JSONL should contain `question` and `answer` (code). Output replaces/augments both fields with Japanese text while preserving code logic.

```
python pipelines/swallow_code/accepted/translate.py \
  --input-jsonl path/to/qa.jsonl \
  --output-jsonl path/to/qa_ja.jsonl \
  --model-path <path-or-HF-ID> \
  --batch-size 4096 \
  --gen-max-tokens 16384 \
  --tensor-parallel-size 1
```

## Dataset Tools

Utilities for preparing public datasets live under `tools/public_datasets/*` (e.g., Wikipedia, Open Code/Math Reasoning, Nemotron) and `tools/converter/*` for Arrow/Parquet → JSONL conversions. Typical usage:

```
python tools/converter/arrow_to_jsonl.py \
  --input path/to/file.arrow \
  --output path/to/file.jsonl
```

See each script’s `--help` for exact arguments.

## Tips and Performance

- Prefer larger batch sizes when GPU memory permits; adjust `--tensor-parallel-size` to spread memory across GPUs.
- `--model-max-length` and `--max-new-tokens` must respect your model’s context window.
- All pipelines stream JSONL in batches to keep memory usage predictable.

## Development

Ruff is configured for linting and formatting.

```
ruff check .
ruff format
ruff --fix .
```

## License

Apache License 2.0. See the `LICENSE` file for details.


[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache2.0-green.svg)](LICENSE)
