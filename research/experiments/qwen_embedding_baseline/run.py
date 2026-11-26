from pathlib import Path
from itertools import combinations
from time import perf_counter
import gc

from research.tools import load_questions
from research.tools import write_results_to_excel

EXPERIMENT_DIR = Path(__file__).resolve().parent
RESEARCH_DIR = EXPERIMENT_DIR.parents[1]
BATCH_SIZES = [1, 2, 4, 8]
INT8_SKIP_MODULES = ["gate_proj", "up_proj", "down_proj"]
RESULTS_DIR = EXPERIMENT_DIR / "results"
MODEL_NAME = "Qwen/Qwen3-Embedding-"
SIZES = ["0.6B", "4B", "8B"]
DATASET_PATH = RESEARCH_DIR / "data" / "sample_answers.json"
PROMPT=""

if __name__ == "__main__":
    questions, errors = load_questions(DATASET_PATH)    # error handling should be added at some point
    
    
    from sentence_transformers import SentenceTransformer
    from transformers import BitsAndBytesConfig
    import torch
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    for BATCH_SIZE in BATCH_SIZES:
        OUTPUT_FILE_NAME = f"batch_size_{BATCH_SIZE}.xlsx"
        rows_by_sheet = {"run": []}
        
        for SIZE in SIZES:
            if device == "cuda":
                torch.cuda.reset_peak_memory_stats()
                
            model_kwargs={"dtype": "auto"}
            if SIZE == "8B": # 8B requires more than 16GB VRAM GPU, which I sadly don't have
                model_kwargs["quantization_config"] = BitsAndBytesConfig(
                                                        load_in_8bit=True,
                                                        llm_int8_skip_modules=INT8_SKIP_MODULES
                                                    )
                
            model = SentenceTransformer(
                model_name_or_path=MODEL_NAME + SIZE,
                device=device,
                model_kwargs=model_kwargs,
            )
            
            rows = []
            encoding_seconds = 0.0
            for question in questions:
                answers = question['answers']
                
                # This version doesn't care about question
                start = perf_counter()
                embeddings = model.encode(
                    [answer['text'] for answer in answers],
                    prompt=PROMPT,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    batch_size=BATCH_SIZE,
                )
                encoding_seconds += perf_counter() - start
                
                
                embeddings = embeddings.astype("float32")
                scores = embeddings @ embeddings.T
                for i, j in combinations(range(len(answers)), 2):
                    score = float(scores[i, j])
                    rows.append(
                        {
                            "question_id": question["id"],
                            "answer_a_id": answers[i]["id"],
                            "answer_b_id": answers[j]["id"],
                            "cosine_similarity": score,
                            "question": question['text'],
                            "answer_a": answers[i]["text"],
                            "answer_b": answers[j]["text"],
                        }               
                    )
                    
            rows_by_sheet[f"Qwen3-Embedding-{SIZE}"] = rows
            run = {
                "model": MODEL_NAME + SIZE,
                "model_revision": model.model_card_data.base_model_revision,
                "quantization": "int8" if SIZE == "8B" else "None",
                "int8_skip_modules": ", ".join(INT8_SKIP_MODULES) if SIZE == "8B" else None,
                "batch_size": BATCH_SIZE,
                "input_format": "answers only",
                "encoding_seconds": encoding_seconds,
                "peak_allocated_gb": torch.cuda.max_memory_allocated() / (1000**3) if device == "cuda" else None,
                "dataset": DATASET_PATH.name,
                "prompt": PROMPT,
                "torch_cuda": torch.version.cuda,
                "pair_count": len(rows),
            }
            rows_by_sheet["run"].append(run)
            del model
            gc.collect()

        write_results_to_excel(RESULTS_DIR / OUTPUT_FILE_NAME, rows_by_sheet)