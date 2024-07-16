import json
import re
import pandas as pd
from fire import Fire
from pathlib import Path
from tqdm.auto import tqdm
from llm_utils.prompts import finetuning_llama3_prompt_template


def format_data(df, output_path, include_answer=True):
    with output_path.open('w') as f:
        for _, row in tqdm(df.iterrows(), total=len(df)):
            doc = row.hypothetical_document
            formatted_answer = finetuning_llama3_prompt_template.format(question=row.question, points=doc, answer=re.sub("([Mr|Mrs|Mdm|Ms|Dr].*?:)", '', row.answer, count=1).strip())                
            if not include_answer:
                formatted_answer = formatted_answer.rsplit('<|end_header_id|>', maxsplit=1)[0] + '<|end_header_id|>'
            f.write(json.dumps({'input': formatted_answer}) + '\n')


def main(input_file_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_hy_doc.jsonl", output_dir_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/"):
    
    input_path = Path(input_file_path)
    output_dir_path = Path(output_dir_path)
    output_dir_path.mkdir(parents=True, exist_ok=True)  


    with input_path.open('r') as f:
        lines = f.readlines()
        
    data = [json.loads(l) for l in lines]
    df_answered = pd.DataFrame(data)

    # only use 2024 data which are answered
    # df_answered = df[df['status'] == 'answered']
    df_answered['date'] = pd.to_datetime(df_answered['filename'].apply(lambda x: x.split('_')[-1]))
    df_answered_2024 = df_answered[df_answered.date.dt.year == 2024]
    df_answered_others = df_answered[df_answered.date.dt.year != 2024]


    print('Train size', len(df_answered_others))
    print('Test size', len(df_answered_2024))

    train_output_path = output_dir_path / Path("hansard_answered_questions_train.csv")
    test_output_path= output_dir_path / Path("hansard_answered_questions_test.csv")

    df_answered_2024.to_csv(test_output_path, index=False)
    df_answered_others.to_csv(train_output_path, index=False)

    # write to llama3 format
    format_data(df_answered_others, output_dir_path / Path("hansard_answered_questions_llama3_formatted_train.jsonl"), include_answer=True)
    format_data(df_answered_2024, output_dir_path / Path("hansard_answered_questions_llama3_formatted_test.jsonl"), include_answer=True)
    format_data(df_answered_2024, output_dir_path / Path("hansard_answered_questions_llama3_formatted_test_no_response.jsonl"), include_answer=False)



if __name__ == "__main__":
    Fire(main)