# ZnajomUJ research

This directory contains experiments on how to score survey answers for participant matching. Each experiment has its own summary with the research question, instructions, results and conclusions.

## Getting started

The research environment is separate from the Django app. The current setup uses Python 3.14. Run these commands from the repository root.

```sh
python3 -m venv research/.venv
research/.venv/bin/python -m pip install -r research/requirements.txt
```

## Directory layout

- `data/` contains experiment inputs.
- `experiments/` contains a folder for each experiment with its script, summary and results.
- `tools/` contains shared helpers for loading, validating and exporting data.

## Experiments

1. [Qwen3-Embedding baseline](experiments/qwen_embedding_baseline/README.md) - we use Qwen embeddings to explore how paraphrasing or negating a Polish survey answer affects its similarity to the original.

