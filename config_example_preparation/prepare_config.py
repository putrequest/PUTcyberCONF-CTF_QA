import json, base64, codecs

import config_strings

# #####################################################################
# EDIT BETWEEN
# #####################################################################

config_template = {
    "workshop": "workshop name",
    "encrypted": True,
    "tasks": [
        {
            "task_id": 1,
            "task_name": config_strings.task_1_name,
            "task_desc": config_strings.task_1_desc,
            "questions": [
                {
                    "q_id": 1,
                    "q_desc": config_strings.task_1_q_1_desc,
                    "q_answer": config_strings.task_1_q_1_answer,
                    "q_hint": config_strings.task_1_q_1_hint,
                },
                {
                    "q_id": 2,
                    "q_desc": None,
                    "q_answer": config_strings.task_1_q_2_answer,
                    "q_hint": config_strings.task_1_q_2_hint
                }
            ]
        }
    ]
}

# #####################################################################

def encode_answer(answer):
    if answer == None:
        return None
    base_encoded = base64.encodebytes(answer.encode('utf-8'))
    str_encoded = codecs.encode(base_encoded.decode('utf-8'), 'rot_13')
    return str_encoded

# encrypting the answers
for task in config_template['tasks']:
    for question in task['questions']:
        question['q_answer'] = encode_answer(question['q_answer'])
        
with open("config.json", "w") as config_file:
    json.dump(config_template, config_file, indent=3, ensure_ascii=False)