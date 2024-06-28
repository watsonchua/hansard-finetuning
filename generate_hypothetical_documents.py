import pandas as pd
import json
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


prompt_template = """Imagine that you are a public servant writing a report for your boss.
Write a report using the following points. Be as elaborate as possible. You can create your own story but it must be around these points and the title:

Title: {title}

Points: {points}
"""

def prompt_model(title, points):
    message = HumanMessage(
        content=prompt_template.format(title=title, points=points)
    )
    return model.invoke([message]).content


with open('written_question_answers_processed.jsonl','r') as f:
    lines = f.readlines()
    
data = [json.loads(l) for l in lines]

df = pd.DataFrame(data)

df_answered = df[df['status'] == 'answered']
df_answered['date'] = pd.to_datetime(df['filename'].apply(lambda x: x.split('_')[-1]))


print(df_answered.groupby(df_answered.date.dt.year).size())


row = df_answered.iloc[0]


print(row.title)
print(row.points)
print(row.question)
print(prompt_model(title=row.title, points=row.points))

with open('written_question_answers_hy_doc.jsonl', 'a') as f:
    for row in tqdm(df_answered.iterrows(), total=len(df_answered)):
        hy_doc = prompt_model(title=row.title, points=row.points)
        new_row_dict = {**row.to_dict(), 'hypothetical_document': hydoc}
        f.write(json.dumps(new_row_dict) + '\n')