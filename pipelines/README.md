<div align="center">

# Pipelines Overview

</div>

This document summarizes the intent and status of each pipeline under `pipelines/`, including which implementations were adopted, which were evaluated only for ablations, and where code intentionally duplicates external repositories for convenience.

## swallow-code

- Purpose: This directory provides the pipeline used for swallow-code-v2. Its implementation intentionally duplicates the logic in the upstream repository for convenience and local experimentation.
- Upstream: https://github.com/rioyokotalab/swallow-code-v2
- Subfolders:
  - `accepted/`: Implementations that were validated as effective via ablation experiments and thus considered as successful methods.
  - `rejected/`: Implementations that did not demonstrate effectiveness in ablation experiments and were not adopted.

Notes:
- Because this is the swallow-code-v2 pipeline, some files closely mirror the upstream repository. This duplication is deliberate to keep all necessary components in one place for reproducibility and controlled modifications.

## swallow_cosmopedia

- Purpose: A data-generation pipeline intended to recreate “Cosmopedia” using Qwen3 instead of Mixtral-8x7B, aiming for higher quality outputs.
- Status: Not adopted. Despite the intention to leverage Qwen3 for improved performance, ablation results did not confirm clear effectiveness, so this pipeline was not selected.

## swallow_math

- Purpose: This directory contains the pipeline used for swallow-math-v2.
- Scripts:
  - `scripts/ablations/`: Data-generation scripts specifically used for ablation experiments. These include methods that were ultimately not adopted.
  - Other scripts outside `scripts/ablations/` were actually used to build swallow-math-v2.

Notes:
- The ablation scripts are retained to document what was tried and to facilitate further investigations and reproducibility, even for approaches that were not selected.

## swallow_wikipedia

- Purpose: A synthetic Q&A data-generation pipeline built from the 2503 Wikipedia dump, designed with the expectation of improving benchmarks such as MMLU and JMMLU.
- Status: Not adopted. Ablation results did not verify effectiveness. In particular, SQuAD-2.0 performance regressed, so this pipeline was not selected.

## General Notes

- Many pipelines process JSONL inputs/outputs and are compatible with vLLM-based generation workflows used elsewhere in this repository.
- “Adopted” vs “not adopted” reflects empirical outcomes from ablation studies rather than implementation quality alone.
