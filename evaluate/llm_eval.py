from anthropic import AnthropicBedrock
from tqdm.auto import tqdm
import pandas as pd



prompt_three_way_template = """Given the following question, context, and three different answers a), b) and c), assess the answer based on the following criteria: 
 1) factual correctness according to the context
 2) similarity to model answer
 3) conciseness
 
Respond in JSON whether answer a), b), or c) is the better answer and state your reason using the following schema:

{{"winner": a, b, or c,
"reason": reason it is the better answer}}

Here is the information,

{question}

Context: {context}

Model Answer: {ground_truth}

Answer A: {answer_a}

Answer B: {answer_b}

Answer C: {answer_c}



Respond with only the JSON reply and nothing else. Use double quotes for the json schema and DO NOT use any double quotes in the values.
"""


prompt_two_way_template = """Given the following question, context, and two different answers a) and b), assess the answer based on the following criteria: 
 1) factual correctness according to the context
 2) similarity to model answer
 3) conciseness
 
Respond in JSON whether answer a) or b) is the better answer and state your reason using the following schema:

{{"winner": a or b,
"reason": reason it is the better answer}}

Here is the information,

{question}

Context: {context}

Model Answer: {ground_truth}

Answer A: {answer_a}

Answer B: {answer_b}

Respond with only the JSON reply and nothing else. Use double quotes for the json schema and DO NOT use any double quotes in the values.
"""

client = AnthropicBedrock()

def query_claude3(prompt):
    message = client.messages.create(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


output_root_dir = '/home/watson_chua/efs/axolotl/data/evaluations/hansard/'
subdir = 'gpt4_normal'
df_all_predictions = pd.read_csv(output_root_dir + subdir + '/consolidated_predictions.csv')


three_way_evaluation_results_claude = []
gpt4_llama3_evaluation_results_claude = []
gpt4_gemma2_evaluation_results_claude = []
llama3_gemma2_evaluation_results_claude = []

df_eval = df_all_predictions
for i, (index, row) in tqdm(enumerate(df_eval.iterrows()), total=len(df_eval)):
    gpt_4_answer = row['gpt4_answer_by_hy_doc']
    ground_truth = row['answer']
    question = row['question']
    hypothetical_doc = row['hypothetical_document']
    llama3_answer = row['llama3_answer']
    gemma2_answer = row['gemma2_answer']


    prompt_three_way = prompt_three_way_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=llama3_answer, answer_c=gemma2_answer)
    prompt_gpt4_llama3 = prompt_two_way_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=llama3_answer)
    prompt_gpt4_gemma2 = prompt_two_way_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=gpt_4_answer, answer_b=gemma2_answer)
    prompt_llama3_gemma2 = prompt_two_way_template.format(context=hypothetical_doc, ground_truth=ground_truth, question=question, answer_a=llama3_answer, answer_b=gemma2_answer)


    try:
        response_three_way = query_claude3(prompt_three_way)
        response_gpt4_llama3 = query_claude3(prompt_gpt4_llama3)
        response_gpt4_gemma2 = query_claude3(prompt_gpt4_gemma2)
        response_llama3_gemma2 = query_claude3(prompt_llama3_gemma2)


    except ValueError as e:
        print(e)
        continue
    
    
    three_way_evaluation_results_claude.append({'claude_evaluation': response_three_way, **row, 'llama3_answer': llama3_answer, 'gemma2_answer': gemma2_answer})
    gpt4_llama3_evaluation_results_claude.append({'claude_evaluation': response_gpt4_llama3, **row, 'llama3_answer': llama3_answer})
    gpt4_gemma2_evaluation_results_claude.append({'claude_evaluation': response_gpt4_gemma2, **row, 'gemma2_answer': gemma2_answer})
    llama3_gemma2_evaluation_results_claude.append({'claude_evaluation': response_llama3_gemma2, **row, 'llama3_answer': llama3_answer, 'gemma2_answer': gemma2_answer})


    import json
    with open(output_root_dir + subdir + '/gpt4_llama3_gemma2_evaluation_claude.jsonl', 'w') as f:
        for l in three_way_evaluation_results_claude:
            f.write(json.dumps(l) + '\n')  

    with open(output_root_dir + subdir + '/gpt4_llama3_evaluation_claude.jsonl', 'w') as f:
        for l in gpt4_llama3_evaluation_results_claude:
            f.write(json.dumps(l) + '\n')  

    with open(output_root_dir + subdir + '/gpt4_gemma2_evaluation_claude.jsonl', 'w') as f:
        for l in gpt4_gemma2_evaluation_results_claude:
            f.write(json.dumps(l) + '\n')  

    with open(output_root_dir + subdir + '/llama3_gemma2_evaluation_claude.jsonl', 'w') as f:
        for l in llama3_gemma2_evaluation_results_claude:
            f.write(json.dumps(l) + '\n')  