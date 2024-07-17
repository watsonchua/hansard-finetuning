# Finetuning LLMs to Draft Parliamentary Responses


## Data Generation
Steps:

1. Crawl Hansard data for written question and answers (code not in this repo). Store in a jsonl file (e.g. `written_question_answers.jsonl`) with each row having these fields:
    - `title`: Title of parliamentary question
    - `question`: Written question that was asked
    - `answer`: Answer to question
    - `filename`: Reference to date of sitting in the format `sitting_YYYY-MM-DD`

    E.g.
    <code>
    {"title": "Proportion of Public Service Agencies that Provide Unpaid Leave for Parents with Multiple or Pre-term Babies", "question": "Mr Louis Ng Kok Kwang asked the Prime Minister (a) what is the number and percentage of public service agencies that provide unpaid leave for parents with multiple or pre-term babies; (b) what is the take-up rate of such leave for each year in the past five years; and (c) if data on the take-up rate has not been collected, whether the Prime Minister's Office will start collecting this data. ", "answer": "In the past five years, an average of 25 officers in the Civil Service utilised this leave provision each year.", "filename": "sitting_2023-02-22"}
    </code>

3. Run `python data_generation/classify_parliamentary_questions.py --model_type "gpt4" --input_file_path <path_to_input_file> --output_file_path <path_to_save_classified_file>` to generate a file with status of whether question is answered, and summary points of answers. Output will be stored in `<path_to_save_classified_file>` (e.g. `written_question_answers_processed.jsonl`)

4. Run `python data_generation/generate_hypotherical_documents.py --model_type "gpt4" --input_file_path <path_to_classified_file> --output_file_path <path_to_save_file_with_hypothetical_docs>` to get the hypothetical documents for each record

5. Run `python data_generation/train_test_split_format.py --input_file_path <path_to_file_with_hypothetical_docs> --output_dir_path <path_to_dir_to_save_train_test_split>` `<path_to_dir_to_save_train_test_split>` will now contain the following files:
    1. `hansard_answered_questions_train.csv` : train data saved as pandas DataFrame
    2. `hansard_answered_questions_test.csv` : test data saved as pandas DataFrame
    3. `hansard_answered_questions_llama3_formatted_train.jsonl` : train data formatted for finetuning
    4. `hansard_answered_questions_llama3_formatted_test.jsonl` : test data formatted for finetuning
    5. `hansard_answered_questions_llama3_formatted_test_no_response.jsonl` : test data formatted for finetuning, with no response (to be used for finetuned models prompt completion)


## Fine-tuning and Prediction

1. Finetune models using axolotl with the above train and test files. These are the config files I used for [Llama-3-8B](https://github.com/watsonchua/axolotl/blob/main/configs/llama-3/lora-8b.yml) and [Gemma-2-9B](https://github.com/watsonchua/axolotl/blob/main/configs/gemma2/lora.yml).
2. After models, have been fine-tuned, get predictions from the models using `hansard_answered_questions_llama3_formatted_test_no_response.jsonl` and save them in the format: `{"generation": <fine-tuned model's generated answer>, "input": <original llama3 formatted input with no response>}`

## Prediction from Pretrained Model
1. Run `bash pretrained_prediction/batch_generate_answers_pretrained.sh` to get the GPT-4o's zero-shot and one-shot answers. SAve them in the same `predictions` folder as the finetuned models.

## Evaluation
