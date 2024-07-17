# Finetuning LLMs to Draft Parliamentary Responses

## Introduction
This repo contains the code for the experiment set-up to fine-tune LLMs on Ha, as described in [this blog post](TBC).
The set-up consists of the following stages, as shown in the diagram below:
- Data Collection and Preprocessing
- Fine-tuning
- Evaluation

![Overall Workflow](image.png)

## Data Collection and Preprocessing
1. **Consolidating written question and answers from Hansard**: Crawl Hansard data for written question and answers (code not in this repo). Store the results in a jsonl file (e.g. `written_question_answers.jsonl`) with each row having these fields:
    - **title**: Title of parliamentary question
    - **question**: Written question that was asked
    - **answer**: Answer to question
    - **filename**: Reference to date of sitting in the format `sitting_YYYY-MM-DD`

    E.g.
    <code>
    {"title": "Proportion of Public Service Agencies that Provide Unpaid Leave for Parents with Multiple or Pre-term Babies", "question": "Mr Louis Ng Kok Kwang asked the Prime Minister (a) what is the number and percentage of public service agencies that provide unpaid leave for parents with multiple or pre-term babies; (b) what is the take-up rate of such leave for each year in the past five years; and (c) if data on the take-up rate has not been collected, whether the Prime Minister's Office will start collecting this data. ", "answer": "In the past five years, an average of 25 officers in the Civil Service utilised this leave provision each year.", "filename": "sitting_2023-02-22"}
    </code>

2. **Classify answers based on whether they answer the questions directly using GPT-4o**: Run `python data_generation/classify_parliamentary_questions.py --model_type "gpt4" --input_file_path <path_to_input_file> --output_file_path <path_to_save_classified_file>` to generate a file with status of whether question is answered, and summary points of answers. Output will be stored in **<path_to_save_classified_file>** (e.g. **written_question_answers_processed.jsonl**)

4. **Generate hypothetical documents as context for answered questions**: Run `python data_generation/generate_hypotherical_documents.py --model_type "gpt4" --input_file_path <path_to_classified_file> --output_file_path <path_to_save_file_with_hypothetical_docs>` to get the hypothetical documents for each record

5. **Split the data into train and test splits, and format them for fine-tuning**: Run `python data_generation/train_test_split_format.py --input_file_path <path_to_file_with_hypothetical_docs> --output_dir_path <path_to_dir_to_save_train_test_split>` **<path_to_dir_to_save_train_test_split>** will now contain the following files:
    1. **hansard_answered_questions_train.csv** : Train data - Pandas DataFrame saved as csv
    2. **hansard_answered_questions_test.csv** : Test data - Pandas DataFrame saved as csv
    3. **hansard_answered_questions_llama3_formatted_train.jsonl** : Train data formatted for finetuning
    4. **hansard_answered_questions_llama3_formatted_test.jsonl** : Test data formatted for finetuning
    5. **hansard_answered_questions_llama3_formatted_test_no_response.jsonl** : Test data formatted for finetuning, with no response (to be used for fine-tuned models prompt completion)


## Fine-tuning and Inference
1. **Fine-tune LLMs**: Fine-tune models using [axolotl](https://github.com/axolotl-ai-cloud/axolotl/tree/main?tab=readme-ov-file#train) with the prompt-formatted train and test files from Step 5 above. These are the config files I used for [Llama-3-8B](https://github.com/watsonchua/axolotl/blob/main/configs/llama-3/lora-8b.yml) and [Gemma-2-9B](https://github.com/watsonchua/axolotl/blob/main/configs/gemma2/lora.yml).


2. **Generate answers using fine-tuned models**: After the models have been fine-tuned, use [axolotl's inference scripts](https://github.com/axolotl-ai-cloud/axolotl/tree/main?tab=readme-ov-file#inference-playground) to generate responses for the test data using the file  **hansard_answered_questions_llama3_formatted_test_no_response.jsonl** as input. Use `<|eot_id|>` as the token for early stopping. Save the responses in the `generation` field as follows, where `input` contains the original prompt-formatted input used for generation:
<code>{"generation": <fine-tuned model's generated answer>, "input": <original llama3 formatted input with no response>}</code>


3. **Generate answers using pre-trained LLM**: To get GPT-4o's zero-shot and one-shot answers, to the same question, by running `python pretrained_prediction/generate_answers_pretrained.py --model_type "gpt4" --one_shot True/False --input_path <path_to_hansard_answered_questions_test_df> --output_file_path <path_so_save_gpt4_answers>` `pretrained_prediction/batch_generate_answers_pretrained.sh` shows an example each on how to generate for zero-shot and one-shot.

## Evaluation
1. **Combine the predictions into a single pandas dataframe**: 

2. **Select better answer using pre-trained LLM**: Use Gemini to select between two answers by running `python evaluation/llm_preference_eval.py --eval_llm_type "gemini" output_dir <path_to_output_dir> --input_file_name <path_to_consolidated_prediction_pandas_df_file> --answer_key_1 <field_for_first_llm_answer> --answer_key_2 <field_for_first_llm_answer> --output_file_prefix <llm1_name_llm2_name>`. Output will be a jsonl file with the fields in the input DataFrame and an additional **evaluation** field containing the JSON string output from the evaluation LLM. E.g.
<code>{"evaluation": "{\"winner\": \"a\", \"reason\": \"Answer A is factually correct as per the context and also matches the model answer. Answer B is factually correct but uses more words to convey the same information and is not as concise as the model answer.\"}}</code>

3. **Compute Ragas scores using pre-trained LLM**: Use Claude-3 Sonnet (Gemini results in too many JSON parsing errors for the Ragas library) to generate the ragas scores by running `python evaluation/ragas_eval.py --eval_llm_type "claude" output_dir <path_to_output_dir> --input_file_name <path_to_consolidated_prediction_pandas_df_file> --answer_key <field_for_llm_answer> --output_file_prefix <llm_name>`. Output will be a pandas dataframe with scores for each record for each of the following metrics:
    - **faithfulness**
    - **answer_relevancy**
    - **answer_similarity**
    - **answer_correctness**

4. **Parse output to get scores**: Use the notebook `evaluation/evaluation_comparison.ipynb` to parse the output and view the scores.

