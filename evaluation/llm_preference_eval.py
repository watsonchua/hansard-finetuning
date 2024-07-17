import pandas as pd
import json
from llm_utils.prompts import three_way_comparison_prompt_template, two_way_comparison_prompt_template
from llm_utils.llms import LLMHelper
from fire import Fire
from tqdm.auto import tqdm
from pathlib import Path


def main(eval_llm_type="claude", output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_normal", input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_normal/consolidated_predictions.csv", answer_key_1="gpt4_answer_by_hy_doc", answer_key_2="llama3_answer", answer_key_3=None, sample_size=None, output_file_prefix="gpt4_zero_shot_llama3"):
    llm_helper = LLMHelper(model_type=eval_llm_type)    
    df_all_predictions = pd.read_csv(input_file_name)
    if sample_size is not None:
        df_all_predictions = df_all_predictions.iloc[:sample_size]
        

    evaluation_results = []

    print(len(df_all_predictions))

        
    for i, (index, row) in tqdm(enumerate(df_all_predictions.iterrows()), total=len(df_all_predictions)):
        ground_truth = row['answer']
        question = row['question']
        hypothetical_doc = row['hypothetical_document']


        if answer_key_3 is not None:
            prompt = three_way_comparison_prompt_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=row[answer_key_1], answer_b=row[answer_key_2], answer_c=row[answer_key_3])
        else:
            prompt = two_way_comparison_prompt_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=row[answer_key_1], answer_b=row[answer_key_2])

        try:
            response = llm_helper.generate(prompt)
        except ValueError as e:
            print(e)
            continue
        
        entry = {'evaluation': response, **row, 'llm1_answer': row[answer_key_1], 'llm2_answer': row[answer_key_2]}
        if answer_key_3 is not None:
            entry['llm3_answer']: row[answer_key_3]
 
        
        evaluation_results.append(entry)

        
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        output_path = output_dir_path/Path(f'{output_file_prefix}_preference_eval_{eval_llm_type}.jsonl')
        
        with output_path.open('w') as f:
            for l in evaluation_results:
                f.write(json.dumps(l) + '\n')  

if __name__ == "__main__":
    Fire(main)