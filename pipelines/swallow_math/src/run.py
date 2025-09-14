from pathlib import Path
import json
import time
from pathlib import Path
from typing import cast

from vllm import LLM, SamplingParams
from transformers import AutoTokenizer, PreTrainedTokenizer
from pipelines.swallow_math.src.prompts import (
    PRE_TRAIN_MATH_TEXT,
    TEXT_BOOK_MATH_TEXT,
    QUESTION_ANSWER_PROMPT,
    PLANNING_APPROACH_PROMPT,
    SOCRATIC_METHOD_PROMPT,
    MULTIPLE_SOLUTION_PROMPT,
)


class MathRewritePipeline:
    def __init__(self, model_name: str, tensor_parallel_size: int, max_model_len: int) -> None:
        self.model_name = model_name
        self.tensor_parallel_size = tensor_parallel_size
        self.max_model_len = max_model_len

        self.llm = LLM(
            model=model_name,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=0.95,
            max_model_len=max_model_len,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer = cast(PreTrainedTokenizer, self.tokenizer)

    def generate(self, prompts: list[str]) -> list[str]:
        params = SamplingParams(temperature=0)
        outputs = self.llm.generate(prompts, params)
        return [output.text for output in outputs]  # type: ignore

    def rewrite_codes(self, texts: list[str], prompt_type: str) -> list[str]:
        prompts: list[str] = []

        if prompt_type == "pre-train-text":
            PROMPT = PRE_TRAIN_MATH_TEXT
        elif prompt_type == "text-book-style":
            PROMPT = TEXT_BOOK_MATH_TEXT
        elif prompt_type == "question-answer":
            PROMPT = QUESTION_ANSWER_PROMPT
        elif prompt_type == "planning-approach":
            PROMPT = PLANNING_APPROACH_PROMPT
        elif prompt_type == "socratic-method":
            PROMPT = SOCRATIC_METHOD_PROMPT
        elif prompt_type == "multiple-solution":
            PROMPT = MULTIPLE_SOLUTION_PROMPT
        else:
            raise ValueError(f"Unsupported prompt_type: {prompt_type}.")

        for text in texts:
            prompt = self.tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": f"### Input\n```\n{text}\n```\n"},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
            prompt = cast(str, prompt)
            prompts.append(prompt)

        tokenized_prompts_len = [len(self.tokenizer.encode(prompt)) for prompt in prompts]
        max_len = max(tokenized_prompts_len)
        if max_len >= self.max_model_len:
            raise ValueError(
                f"Prompt length exceeds model limit: {max_len} >= {self.max_model_len}. "
                "Consider reducing the input size or using a smaller model."
            )
        outputs = self.llm.generate(
            prompts,
            SamplingParams(temperature=0, max_tokens=self.max_model_len - max_len),
        )
        return [output.outputs[0].text for output in outputs]  # type: ignore


def extract_math_text(text: str) -> str:
    """Extract math text from the response"""
    start_marker = "<|MATH_TEXT|>"
    start_index = text.find(start_marker)
    if start_index == -1:
        return text.strip()

    return text[start_index + len(start_marker) :].strip()


def stream_jsonl_math(file_path: Path, batch_size: int = 1024):
    """Stream JSONL file in batches for math processing"""
    batch = []
    with file_path.open("r", encoding="utf-8") as fin:
        for line in fin:
            batch.append(json.loads(line))
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:  # return remaining data
            yield batch


def math_rewrite(
    input_path: Path,
    output_path: Path,
    model_name: str,
    batch_size: int,
    tensor_parallel_size: int,
    model_max_length: int,
    prompt_type: str,
    input_jsonl_key: str = "text",
    llm_output_jsonl_key: str = "llm_output",
    math_text_jsonl_key: str = "math_text",
) -> None:
    """Math text rewriting using GPU processing"""
    pipeline = MathRewritePipeline(
        model_name=model_name,
        tensor_parallel_size=tensor_parallel_size,
        max_model_len=model_max_length,
    )

    total_items = 0
    start_time = time.time()

    print(f"Starting math rewriting with {tensor_parallel_size} GPUs using {prompt_type} prompt...")

    with output_path.open("w", encoding="utf-8") as fout:
        for batch in stream_jsonl_math(input_path, batch_size):
            total_items += len(batch)
            print(f"Processing batch of {len(batch)} items...")

            if not all(input_jsonl_key in item for item in batch):
                raise ValueError(f"All items in the batch must contain {input_jsonl_key} key for math rewriting")
            texts = [item.get(input_jsonl_key, "") for item in batch]

            try:
                rewritten_texts = pipeline.rewrite_codes(texts, prompt_type=prompt_type)

                for index, item in enumerate(batch):
                    rewritten_text = rewritten_texts[index] if index < len(rewritten_texts) else ""
                    extracted_math = extract_math_text(rewritten_text)
                    item[llm_output_jsonl_key] = rewritten_text
                    item[math_text_jsonl_key] = extracted_math
                    fout.write(json.dumps(item, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Error during math rewriting: {e}")

    actual_time = time.time() - start_time
    print(f"Math rewriting completed: {actual_time:.1f}s total ({actual_time / total_items:.3f}s per item)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Swallow Math v2 Pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # math rewrite
    parser = sub.add_parser("math_rewrite", help="math code rewriting")

    parser.add_argument(
        "--input-jsonl",
        type=Path,
        required=True,
        help="Input JSONL file for math rewrite",
    )
    parser.add_argument(
        "--output-jsonl",
        type=Path,
        required=True,
        help="Output JSONL file for math rewrite",
    )
    parser.add_argument(
        "--input-jsonl-key",
        type=str,
        default="text",
        help="Key in JSONL for input text",
    )
    parser.add_argument(
        "--llm-output-jsonl-key",
        type=str,
        default="llm_output",
        help="Key in JSONL for LLM output",
    )
    parser.add_argument(
        "--math-text-jsonl-key",
        type=str,
        default="math_text",
        help="Key in JSONL for extracted math text",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-235B-A22B-Thinking-2507-FP8",
        help="model identifier for vLLM",
    )
    parser.add_argument("--batch-size", type=int, default=4096, help="Batch size for processing")
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=1,
        help="Number of GPUs to use for tensor parallelism",
    )
    parser.add_argument(
        "--model-max-length",
        type=int,
        default=40960,
        help="Maximum model length for rewriting",
    )
    parser.add_argument(
        "--prompt-type",
        type=str,
        default="pre-train-text",
        choices=[
            "pre-train-text",
            "text-book-style",
            "question-answer",
            "planning-approach",
            "socratic-method",
            "multiple-solution",
        ],
        help="Prompt type for math rewriting",
    )

    args = parser.parse_args()
    if args.cmd == "math_rewrite":
        math_rewrite(
            input_path=args.input_jsonl,
            output_path=args.output_jsonl,
            model_name=args.model,
            batch_size=args.batch_size,
            tensor_parallel_size=args.tensor_parallel_size,
            model_max_length=args.model_max_length,
            prompt_type=args.prompt_type,
            input_jsonl_key=args.input_jsonl_key,
            llm_output_jsonl_key=args.llm_output_jsonl_key,
            math_text_jsonl_key=args.math_text_jsonl_key,
        )
    else:
        raise ValueError(f"Unknown command: {args.cmd}")
