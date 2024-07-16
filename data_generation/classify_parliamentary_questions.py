import os
import json
from llm_utils.llms import LLMHelper
from llm_utils.prompts import classify_parliamentary_answer_prompt_template
from llm_utils.post_processing import clean_json_output
from pathlib import Path
from fire import Fire
from tqdm.auto import tqdm


def main(model_type="gpt4", input_file_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers.jsonl", output_file_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_processed.jsonl"):
    input_path = Path(input_file_path)
    output_path = Path(output_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    

    with input_path.open('r') as f:
        lines = f.readlines()
    
    json_lines = [json.loads(l) for l in lines]


    llm_helper = LLMHelper(model_type=model_type)
    
    with output_path.open('a') as f:
        for jl in tqdm(json_lines):
            prompt = classify_parliamentary_answer_prompt_template.format(question=jl['question'], answer=jl['answer'])
            response = llm_helper.generate(prompt)
            json_data = clean_json_output(response)

            try:
                json_test = json.loads(json.dumps(json_data))
            except json.JSONDecodeError as e:        
                print(f"JSON decoding error: {e}")
                continue

            json_data["points"] = '\n\n'.join(json_data["summary_points"])
            for k,v in jl.items():
                if k in json_data:
                    continue
                json_data[k] = v

            f.write(json.dumps(json_data)+'\n') 

if __name__ == "__main__":
    Fire(main)