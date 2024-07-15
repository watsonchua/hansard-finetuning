from tqdm.auto import tqdm
import pandas as pd
from llm_utils.prompts import prompt_three_way_comparison_template, prompt_two_way_comparison_template
from llm_utils.llms import LLMHelper
from fire import Fire


def main(model_type="claude", output_root_dir = '/home/watson_chua/efs/axolotl/data/evaluations/hansard/', subdir = 'gpt4_normal'):
    llm_helper = LLMHelper(model_type=model_type)
    
    df_all_predictions = pd.read_csv(output_root_dir + subdir + '/consolidated_predictions.csv')


    three_way_evaluation_results_claude = []
    gpt4_llama3_evaluation_results_claude = []
    gpt4_gemma2_evaluation_results_claude = []
    llama3_gemma2_evaluation_results_claude = []

    df_eval = df_all_predictions
    print(len(df_eval))
    for i, (index, row) in tqdm(enumerate(df_eval.iterrows()), total=len(df_eval)):
        gpt_4_answer = row['gpt4_answer_by_hy_doc']
        ground_truth = row['answer']
        question = row['question']
        hypothetical_doc = row['hypothetical_document']
        llama3_answer = row['llama3_answer']
        gemma2_answer = row['gemma2_answer']


        prompt_three_way = prompt_three_way_comparison_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=llama3_answer, answer_c=gemma2_answer)
        prompt_gpt4_llama3 = prompt_two_way_comparison_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=llama3_answer)
        prompt_gpt4_gemma2 = prompt_two_way_comparison_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=gemma2_answer)
        prompt_llama3_gemma2 = prompt_two_way_comparison_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=llama3_answer, answer_b=gemma2_answer)


        try:
            response_three_way = llm_helper.generate(prompt_three_way)
            response_gpt4_llama3 = llm_helper.generate(prompt_gpt4_llama3)
            response_gpt4_gemma2 = llm_helper.generate(prompt_gpt4_gemma2)
            response_llama3_gemma2 = llm_helper.generate(prompt_llama3_gemma2)


        except ValueError as e:
            print(e)
            continue
        
        
        three_way_evaluation_results_claude.append({'evaluation': response_three_way, **row, 'llama3_answer': llama3_answer, 'gemma2_answer': gemma2_answer})
        gpt4_llama3_evaluation_results_claude.append({'evaluation': response_gpt4_llama3, **row, 'llama3_answer': llama3_answer})
        gpt4_gemma2_evaluation_results_claude.append({'evaluation': response_gpt4_gemma2, **row, 'gemma2_answer': gemma2_answer})
        llama3_gemma2_evaluation_results_claude.append({'evaluation': response_llama3_gemma2, **row, 'llama3_answer': llama3_answer, 'gemma2_answer': gemma2_answer})


        import json
        with open(output_root_dir + subdir + '/gpt4_llama3_gemma2_evaluation_{model_type}.jsonl', 'w') as f:
            for l in three_way_evaluation_results_claude:
                f.write(json.dumps(l) + '\n')  

        with open(output_root_dir + subdir + '/gpt4_llama3_evaluation_{model_type}.jsonl', 'w') as f:
            for l in gpt4_llama3_evaluation_results_claude:
                f.write(json.dumps(l) + '\n')  

        with open(output_root_dir + subdir + '/gpt4_gemma2_evaluation_{model_type}.jsonl', 'w') as f:
            for l in gpt4_gemma2_evaluation_results_claude:
                f.write(json.dumps(l) + '\n')  

        with open(output_root_dir + subdir + '/llama3_gemma2_evaluation_{model_type}.jsonl', 'w') as f:
            for l in llama3_gemma2_evaluation_results_claude:
                f.write(json.dumps(l) + '\n')  

if __name__ == "__main__":
    Fire(main)