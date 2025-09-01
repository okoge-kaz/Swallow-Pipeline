# EvalPlus

## Evaluation Tasks

- [x] HumanEval
- [x] HumanEval+
- [x] MBPP
- [x] MBPP+

We use HumanEval and HumanEval+ for Python code generation evaluation.

## Setup

**CAUTION**: The Official EvalPlus repository is https://github.com/evalplus/evalplus. However, We use a forked repository for PBS job scripts.

```bash
git clone https://github.com/okoge-kaz/evalplus

uv venv
source .venv/bin/activate

uv pip install --upgrade "evalplus[vllm]"
uv pip install -e .
```

## Usage

### 8B, 14B, 32B models

Please change https://github.com/okoge-kaz/evalplus/blob/master/scripts/rt_HG.sh 's `MODEL_NAME` to your model name.

Then, submit the job:

```bash
qsub -P <group-name> scripts/rt_HG.sh
```

### more than 50B models

Please change https://github.com/okoge-kaz/evalplus/blob/master/scripts/rt_HF.sh 's `MODEL_NAME` to your model name.

Then, submit the job:

```bash
qsub -P <group-name> scripts/rt_HF.sh
```
