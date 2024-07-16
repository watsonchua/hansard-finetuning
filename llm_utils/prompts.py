
################# Classify parliamentary answer #################################################

classify_parliamentary_answer_prompt_template = """Given the following question and answer pair, do the following:
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







################# LLM preference evaluation prompt templates #################################################

three_way_comparison_prompt_template = """Given the following question, context, and three different answers a), b) and c), assess the answer based on the following criteria: 
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


two_way_comparison_prompt_template = """Given the following question, context, and two different answers a) and b), assess the answer based on the following criteria: 
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

################# Zero-shot and One-shot Prompt Templates #################################################


parliamentary_reply_prompt_template = """Imagine that you are a public servant drafting a reply for a parliamentary question.
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

parliamentary_reply_one_shot_example = """Here is an example:

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

################# Prompt Template for Finetuning #################################################


finetuning_llama3_prompt_template = """<|start_header_id|>system<|end_header_id|>You are a public servant. Your task is to reply to a parliamentary question given a list of supporting points.<|eot_id|><|start_header_id|>user<|end_header_id|>
Question:{question}

Supporting points: {points}

<|eot_id|><|start_header_id|>assistant<|end_header_id|>{answer}<|eot_id|><|end_of_text|>"""


################# Prompt Template for Hypothetical Document Generation #################################################

hypothetical_report_from_points_prompt_template = """Imagine that you are a public servant writing a report for your boss.
Write a report using the following points. Be as elaborate as possible. You can create your own story but it must be around these points and the title:

Title: {title}

Points: {points}
"""