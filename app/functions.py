from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QPushButton, QGroupBox, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui
from PyQt6 import QtWidgets as widget

import functools, json, re, sys, base64, codecs, os, getopt

FONT_FAMILY_NAME = "./assets/fonts/AtkinsonHyperlegible-Regular.ttf"
FONT_SIZE_BOX = 14
FONT_SIZE_BOX_DESCRIPTION = 13
FONT_SIZE_INTERNAL = 12

answer_button_list = []

class CounterQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions_done = 0
        self.questions_total = 0
        self.__update()

    def set_question_done(self):
        self.questions_done += 1
        self.__update()

    def set_question_total(self, total: int):
        self.questions_total = total
        self.__update()

    def __update(self):
        self.setText(f"Pytania: {self.questions_done} / {self.questions_total}")

class CustomPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ifDone = False

# other methods

def process_arguments(app: widget.QApplication):
    try:
        opts, args = getopt.getopt(app.arguments()[1:], "c:", ["config="])
        return opts
    except getopt.GetoptError:
        print("Invalid arguments!")
    return None
        
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

def set_app_icon(app: widget.QApplication):
    app_icon = QtGui.QIcon(resource_path("./assets/app_icon/icon.ico"))
    print("app_args:", app.arguments())
    app.setWindowIcon(app_icon)

def decode_answer(answer: str):
    if answer == None:
        return None
    str_decoded = codecs.decode(answer, 'rot_13')
    base_decode = base64.decodebytes(str_decoded.encode('utf-8'))
    return base_decode.decode('utf-8')

def process_task_config(task: dict):
    '''
    Adding None keyword to task dictionary keys, asserting the dictionary will be properly configured in further processing.
    
    - `task_desc` - optional key, None or str
    '''
    if 'task_desc' not in task:
        task['task_desc'] = None
    if 'questions' not in task:
        task['questions'] = []
    return task

def process_question_config(question: dict):
    '''
    Adding None keyword to question dictionary keys, asserting the dictionary will be properly configured in further processing.
    
    - `q_desc` - optional key, None or str
    - `q_answer` - optional key, None or str
    - `q_hint` - optional key, None or str
    - `q_answer_case_sensitive` - optional key, False or True
    '''
    if 'q_desc' not in question:
        question['q_desc'] = None
    if 'q_answer' not in question:
        question['q_answer'] = None
    if 'q_hint' not in question:
        question['q_hint'] = None
    if 'q_answer_case_sensitive' not in question:
        question['q_answer_case_sensitive'] = False
    return question

def read_file(custom_config: str = None):   
    config_location = "config.json"
    
    if custom_config != None:
        for opt in custom_config:
            if opt[0] in ("-c", "--config"):
                config_location = opt[1]
                break   
     
    with open(config_location, "r", encoding='utf-8') as config_file:
        ctf_configs = json.load(config_file)
        
        for task in ctf_configs['tasks']:
            task = process_task_config(task)
            for question in task['questions']:
                question = process_question_config(question)
                # if `encoded` flag set, decode answer
                if 'encrypted' in ctf_configs:
                    if ctf_configs['encrypted'] == None:
                        continue
                    question['q_answer'] = decode_answer(question['q_answer'])
        
        return ctf_configs
    
def reset_progress():
    # go through each task and reset progress
    print("TODO")

def set_check_image(img: QLabel, answer: bool, initial: bool = False):
    if initial:
        img.setPixmap(QtGui.QPixmap(resource_path("./assets/check_icon/circle-question-solid.png")).scaledToWidth(20, mode = Qt.TransformationMode.SmoothTransformation))
        img.setMaximumWidth(25)
        return
    match answer:
        case True: img.setPixmap(QtGui.QPixmap(resource_path("./assets/check_icon/circle-check-solid.png")).scaledToHeight(20, mode = Qt.TransformationMode.SmoothTransformation)),
        case False: img.setPixmap(QtGui.QPixmap(resource_path("./assets/check_icon/circle-xmark-solid.png")).scaledToHeight(20, mode = Qt.TransformationMode.SmoothTransformation))
    return
    
def check_step(question_total_label: CounterQLabel, submit_button: CustomPushButton, step_img: QLabel):
    submit_button.setEnabled(False)
    submit_button.setText("Zrobione")
    submit_button.ifDone = True
    set_check_image(step_img, True)
    question_total_label.set_question_done()
    
    for answer in answer_button_list:
        if not answer.ifDone:
            return
        
    # all answers are correct
    make_message("Gratulacje!", "Wszystkie odpowiedzi są poprawne!", "Zakończono zadanie.", widget.QMessageBox.Icon.Information)

def check_answer(question_total_label: CounterQLabel, submit_button: CustomPushButton, answer_img: QLabel, answer_box: QLineEdit = None, question: dict = None):        
    current_answer = answer_box.text()
    
    orig_answer = question['q_answer']
    
    if question['q_answer_case_sensitive'] and current_answer == orig_answer or not question['q_answer_case_sensitive'] and current_answer.upper() == orig_answer.upper():
        answer_box.setEnabled(False)
        submit_button.setEnabled(False)
        submit_button.setText("Dobrze!")
        submit_button.ifDone = True
        set_check_image(answer_img, True)
        question_total_label.set_question_done()
        
        for answer in answer_button_list:
            if not answer.ifDone:
                return
            
        # all answers are correct
        make_message("Gratulacje!", "Wszystkie odpowiedzi są poprawne!", "Zakończono zadanie.", widget.QMessageBox.Icon.Information)
    else:
        # display error for 1 second
        set_check_image(answer_img, False)
        QTimer.singleShot(500, lambda: set_check_image(answer_img, True, True))
        
def display_hint(hint: str):
    msg_hint = widget.QMessageBox()
    msg_hint.setWindowTitle("Hint")
    msg_hint.setIcon(widget.QMessageBox.Icon.Information)
    msg_hint.setText(hint)
    msg_hint.exec()
    
def generate_placeholder(answer: str):
    return re.sub(r"[\w!]", "*", answer)
        
def populate_task_list(task_layout: QVBoxLayout, title: QLabel, app: QApplication, menu_bar: widget.QMenuBar):
    try:
        task_list = read_file(process_arguments(app))
    
        title.setText(task_list['workshop'])
        
        questions_total_label = CounterQLabel()
        questions_total_label.setStyleSheet("background-color: #4D6357; border-radius: 5px; color: #b6C044; padding: 5px; font-size: 14px;")
        
        menu_bar.setCornerWidget(questions_total_label, Qt.Corner.TopRightCorner)
        
        # sort task list
        task_list = sorted(task_list['tasks'], key=lambda x: x['task_id'])
        
        for task in task_list:
            task_layout.addWidget(set_task(task, questions_total_label))
            
        questions_total_label.set_question_total(len(answer_button_list))
        
    except FileNotFoundError:
        make_message(
            title       = "Brak pliku!",
            main_text   = "Nie znaleziono pliku konfiguracyjnego!",
            sub_text    = "Program się zakończy.",
            icon        = widget.QMessageBox.Icon.Critical
        )
        sys.exit()
        
def make_message(title: str, main_text: str, sub_text: str, icon: widget.QMessageBox.Icon):
    msg_popup = widget.QMessageBox()
    msg_popup.setWindowTitle(title)
    msg_popup.setText(main_text)
    msg_popup.setInformativeText(sub_text)
    msg_popup.setIcon(icon)
    msg_popup.exec()
        
def set_task(task: dict, question_total_label: CounterQLabel):
    '''
    Creating new task with:
    - task_name
    - task_desc - optional
    - questions
    
    returns QGroupBox()
    '''
    
    task_box = QGroupBox()
    task_box.setTitle(task['task_name'])
    # TODO: rethink the borders
    task_box.setStyleSheet("QGroupBox { border: 1px solid #96B024; border-radius: 10px; padding-top: 10px; }")
    
    
    FONT_FAMILY = QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont(resource_path(FONT_FAMILY_NAME)))[0]
    
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
        # if there is description, but no questions
        if len(task['questions']) == 0:
            return task_box
        # if there are questions - add a separator
        task_layout_main.addWidget(task_separator)
    
    # question font setting
    question_font_interal = QtGui.QFont()
    question_font_interal.setFamily(FONT_FAMILY)
    question_font_interal.setPointSize(FONT_SIZE_INTERNAL)
    question_font_interal.setBold(False)
    
    question_list = sorted(task['questions'], key=lambda x: x['q_id'])
    
    for question in question_list:
        if question['q_answer'] == None:
            task_layout_main.addLayout(set_question_step(question, question_font_interal, question_total_label))
            continue
        task_layout_main.addLayout(set_question(question, question_font_interal, question_total_label))
        
    return task_box
        
def set_question(question: dict, font: QtGui.QFont, question_total_label: CounterQLabel):
    layout_question = QHBoxLayout()
    
    question_answer = QLineEdit()
    question_answer.setPlaceholderText(generate_placeholder(question['q_answer']))
    question_answer.setFont(font)
    
    question_answer_indicator = QLabel()
    
    set_check_image(question_answer_indicator, False, True)
    
    inner_layout_answer = QHBoxLayout()
    inner_layout_answer.addWidget(question_answer_indicator)
    inner_layout_answer.addWidget(question_answer)
        
    question_submit = CustomPushButton()
    question_submit.setText("Sprawdź")
    question_submit.clicked.connect(functools.partial(check_answer, question_total_label, question_submit, question_answer_indicator, question_answer, question))
    question_submit.setFont(font)
    answer_button_list.append(question_submit)
    inner_layout_submit = QVBoxLayout()
    inner_layout_submit.addWidget(question_submit)
    
    # enable question approval on enter
    question_answer.returnPressed.connect(functools.partial(check_answer, question_total_label, question_submit, question_answer_indicator, question_answer, question))
    
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

def set_question_step(question: dict, font: QtGui.QFont, question_total_label: CounterQLabel):
    layout_step = QHBoxLayout()
    
    step_indicator = QLabel()
    
    set_check_image(step_indicator, False, True)
    
    step_desc = QLabel(question['q_desc'])
    step_desc.setWordWrap(True)
    step_desc.setTextFormat(Qt.TextFormat.MarkdownText)
    step_desc.setFont(font)
    inner_layout_desc = QHBoxLayout()
    inner_layout_desc.addWidget(step_indicator)
    inner_layout_desc.addWidget(step_desc)
    
    step_submit = CustomPushButton()
    step_submit.setText("Wykonaj")
    step_submit.setFont(font)
    step_submit.clicked.connect(functools.partial(check_step, question_total_label, step_submit, step_indicator))
    answer_button_list.append(step_submit)
    inner_layout_submit = QVBoxLayout()
    inner_layout_submit.addWidget(step_submit)
    
    layout_step.addLayout(inner_layout_desc, 80)
    layout_step.addLayout(inner_layout_submit, 20)
    
    return layout_step