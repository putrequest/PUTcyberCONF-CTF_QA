import json, base64, codecs

class Question():
    def __init__(self, question_desc: str = None, question_answer: str = None, question_hint: str = None, case_sensitive: bool = False):
        self.question_desc = question_desc
        self.question_answer = self.__encode_answer(question_answer)
        self.question_hint = question_hint
        self.case_sensitive = case_sensitive
    
    def __encode_answer(self, answer):
        if answer == None:
            return None
        base_encoded = base64.encodebytes(answer.encode('utf-8'))
        str_encoded = codecs.encode(base_encoded.decode('utf-8'), 'rot_13')
        return str_encoded
        
    def set_desc(self, question_desc: str):
        self.question_desc = question_desc
        
    def set_answer(self, question_answer: str, case_sensitive: bool = False): 
        self.question_answer = self.__encode_answer(question_answer)
        self.case_sensitive = case_sensitive
        
    def set_hint(self, question_hint: str):
        self.question_hint = question_hint

class Task():
    def __init__(self, task_name: str, task_desc: str):
        self.task_name = task_name
        self.task_desc = task_desc     
        
        self.question_list = []
        self.question_enum = 0
        
    def add_question(self, question: Question):
        self.question_list.append({
            "q_id": self.question_enum,
            "q_desc": question.question_desc,
            "q_answer": question.question_answer,
            "q_hint": question.question_hint,
            "q_answer_case_sensitive": question.case_sensitive,
        })
        self.question_enum += 1

class CTF_Config():
    def __init__(self, workshop_name: str, encrypted: bool = False):
        self.workshop_name = workshop_name
        self.encrypted = encrypted
        
        self.task_list = []
        self.task_enum = 0
    
    def add_task(self, task: Task):
        self.task_list.append({
            "task_id": self.task_enum,
            "task_name": task.task_name,
            "task_desc": task.task_desc,
            "questions": task.question_list
        })
        self.task_enum += 1
    
    def __create_config(self):
        config_group = {
            "workshop": self.workshop_name,
            "encrypted": self.encrypted,
            "tasks": self.task_list
        }
        return config_group
        
    def save_config(self):
        with open("config.json", "w") as config_file:
            json.dump(self.__create_config(), config_file, indent=3, ensure_ascii=True)