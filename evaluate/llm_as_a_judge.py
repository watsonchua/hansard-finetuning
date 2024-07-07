import pandas as pd
import json
import os
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from tqdm.auto import tqdm

# os.environ["AZURE_OPENAI_API_KEY"]
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://ai-capdev-oai-eastus-gcc2.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-05-01-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"



model = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
)


prompt_template = """Given the following question, context, and two different answers a) and b), assess the answer based on the following criteria: 
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


Respond with only the reply.
"""

def clean_json_output(output):
    output = output.strip()
    if output.startswith("```json"):
        output = output[7:]
    if output.endswith("```"):
        output = output[:-3]
    cleaned_output = output.strip()

    try:
        json_data = json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        return cleaned_output

    def clean_json(data):
        if isinstance(data, dict):
            return {key: clean_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_json(item) for item in data]
        elif isinstance(data, str):
            return "" if data.lower() in ["unknown", "na", "null"] else data
        else:
            return data

    cleaned_json_data = clean_json(json_data)
    cleaned_output = json.dumps(cleaned_json_data, ensure_ascii=False)

    return cleaned_output


def prompt_model(title, points, question):
    message = HumanMessage(
        content=prompt_template.format(title=title, question=question, points=points)
    )
    return model.invoke([message]).content


def main(input_path, output_path, gpt4_answer_field, finetuned_answer_field, context_field, ground_truth_field):
    
    with open(output_path, 'a') as f:
        with open(input_path, 'r') as f:
            lines = f.readlines()
        
        json_lines = [json.loads(l) for l in lines]
            
            
        for jl in tqdm(json_lines):
            try:
                answer = prompt_model(
                    question=jl['question_field'], 
                    answer=jl['ground_truth_field'], 
                    answer_a=jl['gpt4_answer_field'], 
                    answer_b=jl['finetuned_answer_field'], 
                    context=jl['context_field']
                    )
            except Exception as e:
                print(e)
                continue

            # new_row_dict = {**row.to_dict(), 'gpt4_answer_by_points': answer}
            new_jl = {**jl, **clean_json_output(answer)}
            f.write(json.dumps(new_jl) + '\n')