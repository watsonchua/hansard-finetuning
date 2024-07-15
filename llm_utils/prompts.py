

prompt_three_way_comparison_template = """Given the following question, context, and three different answers a), b) and c), assess the answer based on the following criteria: 
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


prompt_two_way_comparison_template = """Given the following question, context, and two different answers a) and b), assess the answer based on the following criteria: 
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