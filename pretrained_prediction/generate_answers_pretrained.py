import pandas as pd
import json
from tqdm.auto import tqdm
from pathlib import Path
from llm_utils.prompts import parliamentary_reply_prompt_template, parliamentary_reply_one_shot_example
from llm_utils.llms import LLMHelper

from fire import Fire

def main(model_type="gpt4", one_shot=False, input_file_path="/home/watson_chua/efs/axolotl/data/input_data/data/hansard_answered_questions_text.csv", output_file_path="/home/watson_chua/efs/axolotl/data/input_data/data/gpt4_answers_by_hy_doc.jsonl"):
    llm_helper = LLMHelper(model_type=model_type)

    df_test = pd.read_csv(input_file_path)
    output_path = Path(output_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)    
    
    with output_path.open('a') as f:
        for _, row in tqdm(df_test.iterrows(), total=len(df_test)):
            try:
                prompt = parliamentary_reply_prompt_template.format(title=row.title, question=row.question, points=row.points, example=parliamentary_reply_one_shot_example if one_shot else "")
                answer = llm_helper.generate(prompt)
                print(answer)
            except Exception as e:
                print(e)
                continue                
            new_row_dict = {**row.to_dict(), 'gpt4_answer_by_hy_doc': answer}
            new_row_dict['date'] = str(new_row_dict['date'])
            f.write(json.dumps(new_row_dict) + '\n')

if __name__ == "__main__":
    Fire(main)