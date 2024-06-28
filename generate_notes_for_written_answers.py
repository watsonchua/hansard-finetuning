import os
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

# os.environ["AZURE_OPENAI_API_KEY"] 
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://ai-capdev-oai-eastus-gcc2.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-05-01-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"





model = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
)



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
        print(f"JSON decoding error: {e}")
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






prompt_template = """Given the following question and answer pair, do the following:
1. Check if the answer addresses the question. If the answer says something like "This question has been asked before, please refer to another answer." The status will be "repeated" and the reference_answer will be the extracted answer link or document id.
2. If the answer says something like "This will be addressed in future" or "Time is needed for investigation" or "The report will be released in future", the status will be "deferred".
3. If the answer does not answer the question, the status will be "not_answered".
3. If the answer addresses the question, the status will be "answered".
4. If the answer addresses the question, summarise the answer in succint and concise point forms in relation to the question.

Give your answer as a JSON output with the following keys:

"status": answered or not_answered or deferred or repeated,
"reference_answer": reference_link_or_id or "",
"summary_points": summarised points or ""

This is the question:
{question}

And this is the answer:
{answer}
"""


def prompt_model(question, answer):
    message = HumanMessage(
        content=prompt_template.format(question=question, answer=answer)
    )
    return model.invoke([message]).content


import json
with open('written_question_answers.jsonl', 'r') as f:
    lines = f.readlines()
json_lines = [json.loads(l) for l in lines]


sample_lines = json_lines[14:]

from tqdm.auto import tqdm
with open('written_question_answers_processed.jsonl', 'a') as f:
    for jl in tqdm(sample_lines):
        json_out = clean_json_output(prompt_model(question=jl['question'], answer=jl['answer']))
        try:
            json_data = json.loads(json_out)
        except json.JSONDecodeError as e:        
            print(f"JSON decoding error: {e}")
            continue

        json_data["points"] = '\n\n'.join(json_data["summary_points"])
        for k,v in jl.items():
            if k in json_data:
                continue
            json_data[k] = v

        f.write(json.dumps(json_data)+'\n') 