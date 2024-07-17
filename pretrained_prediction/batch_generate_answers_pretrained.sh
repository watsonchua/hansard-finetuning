sample_size_args="--sample_size 3"
# sample_size_args=""

python generate_answers_pretrained.py --model_type "gpt4" --one_shot=False --input_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_hy_doc.jsonl" --output_path="/home/watson_chua/efs/hansard_finetuning/data/predictions/gpt4_answers_by_hy_doc.jsonl" $sample_size_args
python generate_answers_pretrained.py --model_type "gpt4" --one_shot=True --input_path="/home/watson_chua/efs/hansard_finetuning/data/input_data/written_question_answers_hy_doc.jsonl" --output_path="/home/watson_chua/efs/hansard_finetuning/data/predictions/gpt4_answers_by_hy_doc_concise.jsonl" $sample_size_args