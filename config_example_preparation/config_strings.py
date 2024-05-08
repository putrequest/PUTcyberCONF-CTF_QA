from helpers import *

ctf = CTF_Config("Crypto", encrypted=True)

task_1_name = "task_name"
task_1_desc = """
long task description
"""

task_1 = Task(task_1_name, task_1_desc)

task_1_q_1_desc = "First question description"
task_1_q_1_answer = "First question answer"
task_1_q_1_hint = "First question hint"

task_1_q_1 = Question(task_1_q_1_desc, task_1_q_1_answer, task_1_q_1_hint)

task_1_q_2_desc = "Second question description"
task_1_q_2_answer = "Second question answer being case sensitive"

task_1_q_2 = Question(task_1_q_2_desc, task_1_q_2_answer, None, case_sensitive=True)

task_1.add_question(task_1_q_1)
task_1.add_question(task_1_q_2)
ctf.add_task(task_1)

task_2_name = "task_name_2"
task_2 = Task(task_2_name, None)
task_2_q_1_desc = "First step description"
task_2_q_1 = Question(task_2_q_1_desc, None, None)

task_2.add_question(task_2_q_1)

ctf.add_task(task_2)

ctf.save_config()