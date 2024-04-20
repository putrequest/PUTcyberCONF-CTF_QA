from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QPushButton, QGroupBox, QTextBrowser
from PyQt6.QtCore import Qt, QSize, QStandardPaths
from PyQt6 import QtGui
from PyQt6 import QtWidgets as widget

import functools, json

FONT_FAMILY = "Lato"
FONT_SIZE_BOX = 14
FONT_SIZE_BOX_DESCRIPTION = 13
FONT_SIZE_INTERNAL = 12

def read_file():
    with open("config.json", "r", encoding='utf-8') as config_file:
        ctf_configs = json.load(config_file)
        print(ctf_configs)
        return ctf_configs
    
def reset_progress():
    # go through each task and reset progress
    print("TODO")

def check_correctness(submit_button: QPushButton, answer_box: QLineEdit = None, answer: str = None):
    
    # if only a question step - no answer needed
    if answer_box == None:
        submit_button.setEnabled(False)
        submit_button.setText("Zrobione")
        return
        
    current_text = answer_box.text()
    
    if current_text == answer:
        answer_box.setEnabled(False)
        submit_button.setEnabled(False)
        submit_button.setText("Dobrze!")
        
def display_hint(hint: str):
    msg_hint = widget.QMessageBox()
    msg_hint.setWindowTitle("Hint")
    msg_hint.setIcon(widget.QMessageBox.Icon.Information)
    msg_hint.setText(hint)
    msg_hint.exec()
        
def populate_task_list(task_layout: QVBoxLayout):
    task_list = read_file()
    
    # sort task list
    task_list = sorted(task_list['tasks'], key=lambda x: x['task_id'])
    
    for task in task_list:
        task_layout.addWidget(set_task(task))
        
def set_task(task: dict):
    '''
    Creating new task with:
    - task_name
    - task_desc - optional
    - questions
    
    returns QGroupBox()
    '''
    
    task_box = QGroupBox()
    task_box.setTitle(task['task_name'])
    
    # setup fonts
    task_font = task_box.font()
    task_font.setFamily(FONT_FAMILY)
    task_font.setPointSize(FONT_SIZE_BOX)
    task_font.setBold(True)
    
    task_box.setFont(task_font)
    
    # TASK LAYOUT
    task_layout_main = QVBoxLayout(task_box)
    
    if task['task_desc'] != None:
        task_desc = QLabel(task['task_desc'])
        task_desc.setWordWrap(True)
        task_desc.setTextFormat(Qt.TextFormat.MarkdownText)
        
        task_separator = QFrame()
        task_separator.setFrameShape(QFrame.Shape.HLine)
        task_separator.setLineWidth(2)
        task_separator.setStyleSheet("color: grey;")
        
        task_font_desc = task_box.font()
        task_font_desc.setFamily(FONT_FAMILY)
        task_font_desc.setPointSize(FONT_SIZE_BOX_DESCRIPTION)
        task_font_desc.setBold(False)
        task_desc.setFont(task_font_desc)
        
        # wrapping to layout main
        task_layout_main.addWidget(task_desc)
        task_layout_main.addWidget(task_separator)
    
    # question list
    
    question_list = sorted(task['questions'], key=lambda x: x['q_id'])
    
    for question in question_list:
        if question['q_answer'] == None:
            task_layout_main.addLayout(set_question_step(question))
            continue
        task_layout_main.addLayout(set_question(question))
        
    return task_box
        
def set_question(question: dict):
    layout_question = QHBoxLayout()
    
    question_answer = QLineEdit()
    # if there is a placeholder in answer
    if question['q_answer_placeholder'] != None:
        question_answer.setPlaceholderText(question['q_answer_placeholder'])
        
    question_submit = QPushButton()
    question_submit.setText("Sprawdź")
    question_submit.clicked.connect(functools.partial(check_correctness, question_submit, question_answer, question['q_answer']))

    layout_question.addWidget(question_answer)
    layout_question.addWidget(question_submit)
    
    if question['q_hint'] != None:
        question_hint = QPushButton()
        question_hint.setText("Podpowiedź")
        question_hint.clicked.connect(functools.partial(display_hint, question['q_hint']))
        layout_question.addWidget(question_hint)
        
    if question['q_desc'] != None:
        layout_task_question = QVBoxLayout()
        
        question_desc = QLabel(question['q_desc'])
        question_desc.setWordWrap(True)
        question_desc.setTextFormat(Qt.TextFormat.MarkdownText)
        
        desc_font = QtGui.QFont()
        desc_font.setFamily(FONT_FAMILY)
        desc_font.setPointSize(FONT_SIZE_INTERNAL)
        desc_font.setBold(False)
        question_desc.setFont(desc_font)
        
        layout_task_question.addWidget(question_desc)
        layout_task_question.addLayout(layout_question)
        return layout_task_question
    
    return layout_question

def set_question_step(question: dict):
    layout_step = QHBoxLayout()
    
    step_desc = QLabel(question['q_desc'])
    step_desc.setWordWrap(True)
    step_desc.setTextFormat(Qt.TextFormat.MarkdownText)
    
    desc_font = QtGui.QFont()
    desc_font.setFamily(FONT_FAMILY)
    desc_font.setPointSize(FONT_SIZE_INTERNAL)
    desc_font.setBold(False)
    step_desc.setFont(desc_font)
    
    step_submit = QPushButton()
    step_submit.setText("Wykonaj")
    step_submit.clicked.connect(functools.partial(check_correctness, step_submit))
    
    layout_step.addWidget(step_desc)
    layout_step.addWidget(step_submit)
    
    return layout_step    

# def set_task_description(data_desc: str = ""):
#     '''
#     Creating new task with widgets:
#     - task_desc: QLabel - description of the task
#     '''
    
#     task_box = QGroupBox()
#     task_box.setTitle("Klient 1")
    
#     # SETUP FONTS
#     task_font = task_box.font()
#     task_font.setFamily("Lato")
#     task_font.setPointSize(14)
#     task_font.setBold(True)
    
#     task_box.setFont(task_font)
    
#     task_font_internal = task_box.font()
#     task_font_internal.setFamily("Lato")
#     task_font_internal.setPointSize(12)
#     task_font_internal.setBold(False)
    
#     # TASK LAYOUT
#     task_layout_main = QVBoxLayout(task_box)
    
#     if data_desc != "":
#         task_desc = QLabel(data_desc)
#         task_desc.setWordWrap(True)
#         task_desc.setTextFormat(Qt.TextFormat.MarkdownText)
    
#         task_separator = QFrame()
#         task_separator.setFrameShape(QFrame.Shape.HLine)
#         task_separator.setLineWidth(2)
#         task_separator.setStyleSheet("color: red;")
        
#         task_font_desc = task_box.font()
#         task_font_desc.setFamily("Lato")
#         task_font_desc.setPointSize(13)
#         task_font_desc.setBold(False)
#         task_desc.setFont(task_font_desc)
        
#         # wrapping to layout main
#         task_layout_main.addWidget(task_desc)
#         task_layout_main.addWidget(task_separator)
    
#     for el in range(1):
#         task_layout_main.addLayout(set_new_submit(description=False, answer="new", font = task_font_internal))
        
#     return task_box
    
# def set_new_submit(description = False, answer = False, hint = False, font = False):
#     layout_answer = QHBoxLayout()
    
#     task_answer = QLineEdit()
#     task_answer.setPlaceholderText("***********")
    
#     task_submit = QPushButton()
#     task_submit.setText("Sprawdź")
    
#     task_submit.clicked.connect(functools.partial(check_correctness, task_answer, task_submit, answer))

#     layout_answer.addWidget(task_answer)
#     layout_answer.addWidget(task_submit)
    
#     task_answer.setFont(font)
#     task_submit.setFont(font)
    
#     if description:
#         layout_task_answer = QVBoxLayout()
        
#         task_description = QLabel(description)
#         task_description.setWordWrap(True)
#         task_description.setTextFormat(Qt.TextFormat.MarkdownText)
#         task_description.setFont(font)
    
#         layout_task_answer.addWidget(task_description)
#         layout_task_answer.addLayout(layout_answer)
#         return layout_task_answer
    
#     return layout_answer

# def set_new_task_step():
#     '''
#     Creating new task step with widgets:
#     - task_step: QLabel - description of the task step
#     - task_step_completed: QPushButton - submission of step completion
#     '''
    
    

# def set_new_task_submit():
#     '''
#     Creating new task with widgets:
#     - task_desc: QLabel - description of the task
#     - task_answer: QLineEdit - answer field
#     - task_submit: QPushButton - answer submission
#     '''
    
#     task_box = QGroupBox()
#     task_box.setContentsMargins(20, 20, 20, 20)
#     task_box.setTitle("Lorem ipsum")
    
#     task_font = task_box.font()
#     task_font.setFamily("Lato")
#     task_font.setPointSize(13)
#     task_font.setBold(True)
    
#     task_box.setFont(task_font)
    
#     task_font_internal = task_box.font()
#     task_font_internal.setFamily("Lato")
#     task_font_internal.setPointSize(11)
#     task_font_internal.setBold(False)
    
#     task_layout_main = QVBoxLayout(task_box)
    
#     task_desc = QLabel(strings.desc_2)
#     task_desc.setWordWrap(True)
#     task_desc.setTextFormat(Qt.TextFormat.MarkdownText)
    
#     task_separator = QFrame()
#     task_separator.setFrameShape(QFrame.Shape.HLine)
#     task_separator.setLineWidth(2)
#     task_separator.setStyleSheet("color: red;")
    
#     task_layout_answer_area = QHBoxLayout()
    
#     # wrapping to layout main
#     task_layout_main.addWidget(task_desc)
#     task_layout_main.addWidget(task_separator)
#     task_layout_main.addLayout(task_layout_answer_area)
    
#     # populating inner layout
#     task_answer = QLineEdit()
#     task_answer.setPlaceholderText("*** *****")
    
#     task_submit = QPushButton()
#     task_submit.setText("Sprawdź")
    
#     task_submit.clicked.connect(functools.partial(check_correctness, task_answer, task_submit))
    
#     task_layout_answer_area.addWidget(task_answer)
#     task_layout_answer_area.addWidget(task_submit)
    
#     # ------------
#     task_desc.setFont(task_font_internal)
#     task_answer.setFont(task_font_internal)
#     task_submit.setFont(task_font_internal)
    
#     return task_box