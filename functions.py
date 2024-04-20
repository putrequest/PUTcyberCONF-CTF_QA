from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QPushButton, QGroupBox, QTextBrowser
from PyQt6.QtCore import Qt, QSize, QStandardPaths
from PyQt6 import QtGui
from PyQt6 import QtWidgets as widget

import functools, json, re, pathlib, sys

FONT_FAMILY = "Lato"
FONT_SIZE_BOX = 14
FONT_SIZE_BOX_DESCRIPTION = 13
FONT_SIZE_INTERNAL = 12

def read_file():
    if sys.platform == "linux":
        with open(pathlib.Path("/usr/CTF_config", "config.json"), "r", encoding='utf-8') as config_file:
            ctf_configs = json.load(config_file)
            return ctf_configs
    else:
        with open(pathlib.WindowsPath("C:", "CTF_config", "config.json"), "r", encoding='utf-8') as config_file:
            ctf_configs = json.load(config_file)
            return ctf_configs
    
def reset_progress():
    # go through each task and reset progress
    print("TODO")
    
def check_step(submit_button: QPushButton):
    submit_button.setEnabled(False)
    submit_button.setText("Zrobione")

def check_answer(submit_button: QPushButton, answer_box: QLineEdit = None, answer: str = None):        
    current_text = answer_box.text()
    
    if current_text == answer or current_text.upper() == answer.upper():
        answer_box.setEnabled(False)
        submit_button.setEnabled(False)
        submit_button.setText("Dobrze!")
        
def display_hint(hint: str):
    msg_hint = widget.QMessageBox()
    msg_hint.setWindowTitle("Hint")
    msg_hint.setIcon(widget.QMessageBox.Icon.Information)
    msg_hint.setText(hint)
    msg_hint.exec()
    
def generate_placeholder(answer: str):
    return re.sub(r"[\w!]", "*", answer)
        
def populate_task_list(task_layout: QVBoxLayout, title: QLabel):
    try:
        task_list = read_file()
    
        title.setText(task_list['workshop'])
        
        # sort task list
        task_list = sorted(task_list['tasks'], key=lambda x: x['task_id'])
        
        for task in task_list:
            task_layout.addWidget(set_task(task))
    except FileNotFoundError:
        msg_no_config_file = widget.QMessageBox()
        msg_no_config_file.setWindowTitle("Brak pliku!")
        msg_no_config_file.setText("Nie znaleziono pliku konfiguracyjnego!")
        msg_no_config_file.setInformativeText("Program się zakończy.")
        msg_no_config_file.setIcon(widget.QMessageBox.Icon.Critical)
        msg_no_config_file.exec()
        sys.exit()
        
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
    
    question_font_interal = QtGui.QFont()
    question_font_interal.setFamily(FONT_FAMILY)
    question_font_interal.setPointSize(FONT_SIZE_INTERNAL)
    question_font_interal.setBold(False)
    
    question_list = sorted(task['questions'], key=lambda x: x['q_id'])
    
    for question in question_list:
        if question['q_answer'] == None:
            task_layout_main.addLayout(set_question_step(question, question_font_interal))
            continue
        task_layout_main.addLayout(set_question(question, question_font_interal))
        
    return task_box
        
def set_question(question: dict, font: QtGui.QFont):
    layout_question = QHBoxLayout()
    
    question_answer = QLineEdit()
    question_answer.setPlaceholderText(generate_placeholder(question['q_answer']))
    question_answer.setFont(font)
    inner_layout_answer = QVBoxLayout()
    inner_layout_answer.addWidget(question_answer)
        
    question_submit = QPushButton()
    question_submit.setText("Sprawdź")
    question_submit.clicked.connect(functools.partial(check_answer, question_submit, question_answer, question['q_answer']))
    question_submit.setFont(font)
    inner_layout_submit = QVBoxLayout()
    inner_layout_submit.addWidget(question_submit)

    # layout_question.addWidget(question_answer)
    # layout_question.addWidget(question_submit)
    
    if question['q_hint'] != None:
        question_hint = QPushButton()
        question_hint.setText("Podpowiedź")
        question_hint.clicked.connect(functools.partial(display_hint, question['q_hint']))
        question_hint.setFont(font)
        inner_layout_hint = QVBoxLayout()
        inner_layout_hint.addWidget(question_hint)
        # layout_question.addWidget(question_hint)
        
        layout_question.addLayout(inner_layout_answer, 60)
        layout_question.addLayout(inner_layout_submit, 20)
        layout_question.addLayout(inner_layout_hint, 20)
    else:
        layout_question.addLayout(inner_layout_answer, 80)
        layout_question.addLayout(inner_layout_submit, 20)
        
    if question['q_desc'] != None:
        layout_task_question = QVBoxLayout()
        
        question_desc = QLabel(question['q_desc'])
        question_desc.setWordWrap(True)
        question_desc.setTextFormat(Qt.TextFormat.MarkdownText)
        question_desc.setFont(font)
        
        layout_task_question.addWidget(question_desc)
        layout_task_question.addLayout(layout_question)
        return layout_task_question
    
    return layout_question

def set_question_step(question: dict, font: QtGui.QFont):
    layout_step = QHBoxLayout()
    
    step_desc = QLabel(question['q_desc'])
    step_desc.setWordWrap(True)
    step_desc.setTextFormat(Qt.TextFormat.MarkdownText)
    step_desc.setFont(font)
    inner_layout_desc = QVBoxLayout()
    inner_layout_desc.addWidget(step_desc)
    
    step_submit = QPushButton()
    step_submit.setText("Wykonaj")
    step_submit.setFont(font)
    step_submit.clicked.connect(functools.partial(check_step, step_submit))
    inner_layout_submit = QVBoxLayout()
    inner_layout_submit.addWidget(step_submit)
    
    layout_step.addLayout(inner_layout_desc, 80)
    layout_step.addLayout(inner_layout_submit, 20)
    
    return layout_step