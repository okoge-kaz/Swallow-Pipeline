#!/bin/bash

hf upload  tokyotech-llm/nemotron-post-training-v1 \
  /groups/gch51639/fujii/datasets/raw/instruct/swallow/nemotron-post-training-v1/code \
  code \
  --repo-type dataset

hf upload  tokyotech-llm/nemotron-post-training-v1 \
  /groups/gch51639/fujii/datasets/raw/instruct/swallow/nemotron-post-training-v1/math \
  math \
  --repo-type dataset

hf upload  tokyotech-llm/nemotron-post-training-v1 \
  /groups/gch51639/fujii/datasets/raw/instruct/swallow/nemotron-post-training-v1/stem \
  stem \
  --repo-type dataset
