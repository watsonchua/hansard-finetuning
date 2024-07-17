import pandas as pd
from datasets import Dataset
from ragas import evaluate
from fire import Fire
from llm_utils.llms import LLMHelper, EmbeddingsHelper
from pathlib import Path
# from ragas.metrics.critique import harmfulness
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    # context_precision,
    # context_recall,
    answer_similarity,
    answer_correctness,
)

# list of metrics we"re going to use
metrics = [
    faithfulness,
    # context_precision,
    # context_recall,
    # harmfulness,
    answer_relevancy,
    answer_similarity,
    answer_correctness,
]

def create_dataset(df_eval, answer_key):
    df_temp = df_eval[["question", answer_key, "hypothetical_document", "answer"]] 
    df_temp["contexts"] = df_eval.apply(lambda x: [x["hypothetical_document"]], axis=1)
    df_temp.rename(columns={answer_key: "answer", "answer": "ground_truth"}, inplace=True)

    ds = Dataset.from_pandas(df_temp, split="eval")
    return ds


def main(eval_llm_type="claude", output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_normal", input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_normal/consolidated_predictions.csv", answer_key="gpt4_answer_by_hy_doc", sample_size=None, output_file_prefix="gpt4_zero_shot"):
    df_all_predictions = pd.read_csv(input_file_name)
    
    if sample_size is not None:
        df_all_predictions = df_all_predictions.iloc[:sample_size]

    eval_dataset = create_dataset(df_all_predictions, answer_key)

    llm_helper = LLMHelper(model_type=eval_llm_type)
    embeddings_helper = EmbeddingsHelper(model_type=eval_llm_type)

    model = llm_helper.model
    embeddings = embeddings_helper.embeddings

    eval_result = evaluate(
        eval_dataset,
        metrics=metrics,
        llm=model,
        embeddings=embeddings,
        raise_exceptions=False
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    eval_result.to_pandas().to_csv(output_path / Path(f"{output_file_prefix}_ragas_{eval_llm_type}.csv"), index=False)

if __name__ == "__main__":
    Fire(main)