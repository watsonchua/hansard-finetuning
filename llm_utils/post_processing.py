import re
import json

def replace_inner_quotes(text):
    split_result  = re.split("\"\s*reason\s*\"", text, maxsplit=1)
    winner_str = split_result[0] 
    reason_str = split_result[1][split_result[1].index('"')+1: split_result[1].rfind('"')].replace('"','').replace("\\", "")
    return winner_str + "\"reason\": \"" + reason_str.strip() + '"}'

def clean_json_output(output):
    output = output.strip()
    if output.startswith("```json"):
        output = output[7:]
    if output.endswith("```"):
        output = output[:-3]
    cleaned_output = replace_inner_quotes(output.strip())
    # cleaned_output = output.strip()


    try:
        json_data = json.loads(cleaned_output, strict=False)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(cleaned_output)
        return cleaned_output

    def clean_json(data):
        if isinstance(data, dict):
            return {key: clean_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_json(item) for item in data]
        elif isinstance(data, str):
            return "" if data.lower() in ["unknown", "na", "null"] else data
        else:
            print(data)
            return data
    
    cleaned_json_data = clean_json(json_data)
    # cleaned_output = json.dumps(cleaned_json_data, ensure_ascii=False)

    return cleaned_json_data