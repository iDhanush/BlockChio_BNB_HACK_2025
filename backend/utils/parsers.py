import ast


def convert_to_dict(json_str):
    if json_str.startswith("```json"):
        json_str = json_str.replace("```json", "").replace("```", "")
    else:
        return json_str
    return ast.literal_eval(json_str)
