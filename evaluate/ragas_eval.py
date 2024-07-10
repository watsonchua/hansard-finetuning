from langchain_aws.chat_models import BedrockChat
from langchain_aws.embeddings import BedrockEmbeddings
from datasets import Dataset
from ragas import evaluate
import pandas as pd
from fire import Fire


from ragas.metrics import (
    context_precision,
    faithfulness,
    answer_relevancy,
    context_recall,
    answer_similarity,
    answer_correctness,
)
# from ragas.metrics.critique import harmfulness

# list of metrics we're going to use
metrics = [
    faithfulness,
    context_precision,
    answer_relevancy,
    context_recall,
    # harmfulness,
    answer_similarity,
    answer_correctness,
]

def create_dataset(df_eval, answer_key):
    df_temp = df_eval[["question", answer_key, "hypothetical_document", "answer"]] 
    df_temp["contexts"] = df_eval.apply(lambda x: [x["hypothetical_document"]], axis=1)
    df_temp.rename(columns={answer_key: "answer", "answer": "ground_truth"}, inplace=True)

    ds = Dataset.from_pandas(df_temp, split="eval")
    return ds


def main(output_root_dir='/home/watson_chua/efs/axolotl/data/evaluations/hansard/', subdir='gpt4_normal'):

    df_all_predictions = pd.read_csv(output_root_dir + subdir + '/consolidated_predictions.csv')
    dataset_gpt4 = create_dataset(df_all_predictions, "gpt4_answer_by_hy_doc")
    dataset_llama3 = create_dataset(df_all_predictions, "llama3_answer")
    dataset_gemma2 = create_dataset(df_all_predictions, "gemma2_answer")

    config = {
        "credentials_profile_name": "default",  # E.g "default"
        "region_name": "us-east-1",  # E.g. "us-east-1"
        "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",  # E.g "anthropic.claude-v2"
        "model_kwargs": {"temperature": 0.01},
    }

    bedrock_model = BedrockChat(
        credentials_profile_name=config["credentials_profile_name"],
        region_name=config["region_name"],
        endpoint_url=f"https://bedrock-runtime.{config['region_name']}.amazonaws.com",
        model_id=config["model_id"],
        model_kwargs=config["model_kwargs"],
    )

    # init the embeddings
    bedrock_embeddings = BedrockEmbeddings(
        credentials_profile_name=config["credentials_profile_name"],
        region_name=config["region_name"],
        model_id="cohere.embed-english-v3",
        endpoint_url=f"https://bedrock-runtime.{config['region_name']}.amazonaws.com",
    )




    gpt4_result = evaluate(
        dataset_gpt4,
        metrics=metrics,
        llm=bedrock_model,
        embeddings=bedrock_embeddings
    )


    llama3_result = evaluate(
        dataset_llama3,
        metrics=metrics,
        llm=bedrock_model,
        embeddings=bedrock_embeddings,
    )


    gemma2_result = evaluate(
        dataset_gemma2,
        metrics=metrics,
        llm=bedrock_model,
        embeddings=bedrock_embeddings,
    )

    gpt4_result.to_pandas().to_csv(output_root_dir + subdir + '/gpt4_ragas_claude.csv', index=False)
    llama3_result.to_pandas().to_csv(output_root_dir + subdir + '/llama3_ragas_claude.csv', index=False)
    gemma2_result.to_pandas().to_csv(output_root_dir + subdir + '/llama3_ragas_claude.csv', index=False)


if __name__ == "__main__":
    Fire(main)