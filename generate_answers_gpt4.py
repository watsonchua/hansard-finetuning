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


prompt_template = """Imagine that you are a public servant drafting a reply for a parliamentary question.
Write a reply given the following:

Title: {title}

Question: {question}

Points: {points}


Respond with only the reply.
"""

def prompt_model(title, points, question):
    message = HumanMessage(
        content=prompt_template.format(title=title, question=question, points=points)
    )
    return model.invoke([message]).content


with open('data/written_question_answers_processed.jsonl','r') as f:
    lines = f.readlines()
    
data = [json.loads(l) for l in lines]

df = pd.DataFrame(data)

df_answered = df[df['status'] == 'answered']
df_answered['date'] = pd.to_datetime(df['filename'].apply(lambda x: x.split('_')[-1]))
df_answered_2024 = df_answered[df_answered.date.dt.year == 2024]

# print(df_answered.groupby(df_answered.date.dt.year).size())


# row = df_answered.iloc[0]


# print(row.title)
# print(row.points)
# print(row.question)
# print(prompt_model(title=row.title, points=row.points))

with open('data/gpt4_answers_by_points.jsonl', 'a') as f:
    for _, row in tqdm(df_answered_2024.iterrows(), total=len(df_answered)):
        try:
            answer = prompt_model(title=row.title, points=row.points, question=row.question)
        except Exception as e:
            print(e)
            continue
            
        new_row_dict = {**row.to_dict(), 'gpt4_answer_by_points': answer}
        new_row_dict['date'] = str(new_row_dict['date'])
        f.write(json.dumps(new_row_dict) + '\n')