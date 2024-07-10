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


one_shot_example = """Here is an example:

Title: 

Fire incidents relate to kitchen exhaust ducts (KED)

Question: 

Mr Zhulkarnain Abdul Rahim asked the Minister for Home Affairs (a) in the past five years, how many fire incidents relate to kitchen exhaust ducts (KED) in food and beverage establishments like coffeeshops or hawker stalls; and (b) for such cases, what is the average prior duration when such KED was last cleaned or maintained by the operators or owners.

Points: 

### Fire Incidents Related to Kitchen Exhaust Ducts in Food and Beverage Establishments

#### Introduction

This report provides an analysis of fire incidents related to kitchen exhaust ducts in food and beverage establishments over the period from 2018 to 2022. The data points to significant patterns and potential areas for improvement in maintenance practices that could mitigate future risks.

#### Executive Summary

Between 2018 and 2022, there were a total of 60 fire incidents involving kitchen exhaust ducts in food and beverage establishments. The average duration between these fire incidents and the last cleaning and maintenance of the ducts was found to be five months. This report delves into the specifics of these incidents, examining the causes, the impact on businesses, and recommendations for future preventative measures.

#### Incident Analysis

Over the five-year period, 60 fires were reported across various types of food and beverage establishments, including restaurants, cafes, and fast-food outlets. These incidents were geographically widespread, affecting both urban and rural establishments alike. 

- **Yearly Breakdown of Incidents:**
  - **2018:** 10 incidents
  - **2019:** 12 incidents
  - **2020:** 15 incidents
  - **2021:** 11 incidents
  - **2022:** 12 incidents

The data indicates a peak in 2020, potentially attributable to operational changes during the COVID-19 pandemic, which might have affected routine maintenance schedules.

#### Maintenance and Cleaning Practices

The average duration between the fire incidents and the last cleaning and maintenance of these ducts was five months. This highlights a critical gap in the maintenance frequency recommended by industry standards. 

- **Industry Standard Recommendations:** 
  - Monthly inspections of kitchen exhaust systems.
  - Quarterly cleaning for systems under heavy use.
  - Semi-annual cleaning for systems under moderate use.

The disparity between the actual maintenance intervals and the recommended schedules suggests a need for stricter adherence to industry guidelines.

#### Causes and Contributing Factors

Several factors contributed to the fire incidents:
- **Accumulation of Grease and Debris:** The primary cause of these fires was the buildup of grease and debris in the exhaust ducts, which are highly flammable.
- **Inadequate Cleaning Procedures:** Many establishments were found to have inadequate cleaning procedures or used unqualified personnel for maintenance tasks.
- **High-Temperature Cooking Methods:** Establishments employing high-temperature cooking methods such as grilling and frying were more prone to grease accumulation, thereby increasing fire risk.
- **Lack of Awareness:** There was a noticeable lack of awareness among business owners and managers regarding the importance of regular maintenance and the risks associated with neglecting it.

#### Impact on Businesses

The impact of these fire incidents on the affected establishments was significant:
- **Financial Losses:** Direct financial losses included property damage, loss of inventory, and business interruption costs. 
- **Reputation Damage:** Many establishments suffered reputation damage, leading to a loss of customer trust and a decline in patronage.
- **Insurance Implications:** The incidents also had implications for insurance premiums and coverage, with some establishments facing increased premiums or difficulty obtaining coverage post-incident.

#### Recommendations

To mitigate future risks and enhance safety in food and beverage establishments, the following recommendations are proposed:
1. **Regular Training and Awareness Programs:** Implement regular training sessions for kitchen staff and management on the importance of exhaust duct maintenance and fire safety.
2. **Adherence to Maintenance Schedules:** Strictly adhere to industry-recommended maintenance and cleaning schedules, ensuring that kitchen exhaust systems are inspected and cleaned by qualified professionals.
3. **Implementation of Monitoring Systems:** Install monitoring systems to track grease buildup and alert management when cleaning is necessary.
4. **Enhanced Regulations and Enforcement:** Advocate for enhanced regulations and enforcement mechanisms to ensure compliance with maintenance standards.
5. **Insurance Incentives:** Work with insurance companies to provide incentives for establishments that maintain regular cleaning schedules and implement fire prevention measures.

#### Conclusion

The analysis of fire incidents related to kitchen exhaust ducts in food and beverage establishments from 2018 to 2022 underscores the critical need for regular maintenance and adherence to industry standards. By implementing the recommended measures, establishments can significantly reduce the risk of fire incidents, ensuring the safety of their operations, employees, and patrons.

#### Appendices

- **Appendix A:** Detailed Yearly Incident Reports
- **Appendix B:** Industry Standard Maintenance Guidelines
- **Appendix C:** Case Studies of Affected Establishments

---

This report highlights the urgent need for improved maintenance practices and regulatory oversight to prevent future fire incidents in food and beverage establishments, ensuring a safer environment for all stakeholders involved.

Reply:

From 2018 to 2022, there were a total of 60 fires involving kitchen exhaust ducts in food and beverage establishments. The average duration between the fire incidents and when these ducts were last cleaned and maintained prior to the fire incidents is five months.

##################################################################################################################
"""

prompt_template = """Imagine that you are a public servant drafting a reply for a parliamentary question.
Given the following title, question, and points, write a reply to the question. 
Respond with only the answer to the question.


Title: 

{title}

Question: 

{question}

Points: 

{points}

######################################################################################################################

{example}

"""

def prompt_model(title, points, question, one_shot=False):
    message = HumanMessage(
        content=prompt_template.format(title=title, question=question, points=points, example=one_shot_example if one_shot else "")
    )
    return model.invoke([message]).content


with open('/home/watson_chua/efs/axolotl/data/input_data/data/written_question_answers_hy_doc.jsonl','r') as f:
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

# with open('data/gpt4_answers_by_points.jsonl', 'a') as f:
with open('/home/watson_chua/efs/axolotl/data/input_data/data/gpt4_answers_by_hy_doc_2.jsonl', 'a') as f:
    for _, row in tqdm(df_answered_2024.iterrows(), total=len(df_answered_2024)):
        try:
            # answer = prompt_model(title=row.title, points=row.points, question=row.question)
            answer = prompt_model(title=row.title, points=row.hypothetical_document, question=row.question, one_shot=False)
            print(answer)
        except Exception as e:
            print(e)
            continue
            
        # new_row_dict = {**row.to_dict(), 'gpt4_answer_by_points': answer}
        new_row_dict = {**row.to_dict(), 'gpt4_answer_by_hy_doc': answer}
        new_row_dict['date'] = str(new_row_dict['date'])
        f.write(json.dumps(new_row_dict) + '\n')