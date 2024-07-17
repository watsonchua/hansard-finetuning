# sample_size_args="--sample_size 3"
sample_size_args=""
model_type="gpt4"
written_question_answer_with_hyd_fp="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_hy_doc.jsonl"
predictions_dir="/home/watson_chua/efs/hansard_finetuning/data/predictions"

python generate_answers_pretrained.py --model_type $model_type --one_shot False --input_file_path $written_question_answer_with_hyd_fp --output_path ${predictions_dir}/gpt4_answers_zero_shot.jsonl $sample_size_args
python generate_answers_pretrained.py --model_type $model_type --one_shot True --input_file_path $written_question_answer_with_hyd_fp --output_path ${predictions_dir}/gpt4_answers_one_shot.jsonl $sample_size_args
