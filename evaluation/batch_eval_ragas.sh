#sample_size_arg="--sample_size 3"
sample_size_arg=""
eval_llm_type="claude"
evaluation_output_dir="/home/watson_chua/efs/hansard_finetuning/data/evaluations"
consolidated_input_fp="/home/watson_chua/efs/hansard_finetuning/data/predictions/consolidated_predictions.csv"

python ragas_eval.py --eval_llm_type="claude" --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp  --answer_key="gpt4_zero_shot_answer" --output_file_prefix "gpt4_zero_shot" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key="gpt4_one_shot_answer" --output_file_prefix "gpt4_one_shot" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key="llama3_answer" --output_file_prefix "llama3" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir $evaluation_output_dir  --input_file_name $consolidated_input_fp --answer_key="gemma2_answer" --output_file_prefix "gemma2" $sample_size_arg