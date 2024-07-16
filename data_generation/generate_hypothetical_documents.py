import pandas as pd
import json
from tqdm.auto import tqdm
from llm_utils.prompts import hypothetical_report_from_points_prompt_template
from llm_utils.llms import LLMHelper
from pathlib import Path
from fire import Fire


def main(model_type="gpt4", input_file_path='/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_processed.jsonl', output_file_path='/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_hy_doc.jsonl'):
    input_path = Path(input_file_path)
    output_path = Path(output_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open('r') as f:
        lines = f.readlines()
        
    data = [json.loads(l) for l in lines]

    df = pd.DataFrame(data)
    df_answered = df[df['status'] == 'answered']

    llm_helper = LLMHelper(model_type=model_type)

    with output_path.open('a') as f:
        for _, row in tqdm(df_answered.iterrows(), total=len(df_answered)):
            try:
                prompt = hypothetical_report_from_points_prompt_template.format(title=row.title, points=row.points)
                hy_doc = llm_helper.generate(prompt)
            except Error as e:
                print(e)
                continue
                
            new_row_dict = {**row.to_dict(), 'hypothetical_document': hy_doc}
            f.write(json.dumps(new_row_dict) + '\n')

if __name__ == "__main__":
    Fire(main)