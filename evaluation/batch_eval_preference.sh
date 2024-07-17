#sample_size_arg="--sample_size 3"
sample_size_arg=""
eval_llm_type="gemini"
evaluation_output_dir="/home/watson_chua/efs/hansard_finetuning/data/evaluations"
consolidated_input_fp="/home/watson_chua/efs/hansard_finetuning/data/predictions/consolidated_predictions.csv"

python llm_preference_eval.py --eval_llm_type $eval_llm_type --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key_1 "gpt4_zero_shot_answer" --answer_key_2 "llama3_answer" --output_file_prefix "gpt4_zero_shot_llama3" $sample_size_arg
python llm_preference_eval.py --eval_llm_type $eval_llm_type --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key_1 "gpt4_zero_shot_answer" --answer_key_2 "gemma2_answer" --output_file_prefix "gpt4_zero_shot_gemma2" $sample_size_arg
python llm_preference_eval.py --eval_llm_type $eval_llm_type --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key_1 "gpt4_one_shot_answer" --answer_key_2 "llama3_answer" --output_file_prefix "gpt4_one_shot_llama3" $sample_size_arg
python llm_preference_eval.py --eval_llm_type $eval_llm_type --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key_1 "gpt4_one_shot_answer" --answer_key_2 "gemma2_answer" --output_file_prefix "gpt4_one_shot_gemma2" $sample_size_arg
python llm_preference_eval.py --eval_llm_type $eval_llm_type --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key_1 "llama3_answer" --answer_key_2 "gemma2_answer" --output_file_prefix "llama3_gemma2" $sample_size_arg

