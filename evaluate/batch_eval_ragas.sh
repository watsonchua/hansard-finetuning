sample_size_arg="--sample_size 3"
# sample_size_arg=""

python ragas_eval.py --eval_llm_type="claude" --output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/temp"  --input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_normal/consolidated_predictions.csv" --answer_key="gpt4_answer_by_hy_doc" --output_file_prefix "gpt4_zero_shot" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/temp"  --input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_concise/consolidated_predictions.csv" --answer_key="gpt4_answer_by_hy_doc" --output_file_prefix "gpt4_one_shot" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/temp"  --input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_concise/consolidated_predictions.csv" --answer_key="llama3_answer" --output_file_prefix "llama3" $sample_size_arg
python ragas_eval.py --eval_llm_type="claude" --output_dir="/home/watson_chua/efs/axolotl/data/evaluations/hansard/temp"  --input_file_name="/home/watson_chua/efs/axolotl/data/evaluations/hansard/gpt4_concise/consolidated_predictions.csv" --answer_key="gemma2_answer" --output_file_prefix "gemma2" $sample_size_arg