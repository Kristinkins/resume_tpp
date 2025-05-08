from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QDateEdit,
    QTextEdit, QPushButton, QLabel, QHBoxLayout, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator
from datetime import date
from ...core.models import WorkExperience, Education, Skill
from ...core import utils


class PersonalInfoForm(QWidget):
    data_changed = pyqtSignal(str, object)

    def __init__(self, resume):
        super().__init__()
        self.resume = resume
        self.init_ui()
        self.set_data(resume)

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля личной информации
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Иванов Иван Иванович")
        self.name_edit.textChanged.connect(lambda: self.emit_data("name"))

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("example@email.com")
        self.email_edit.textChanged.connect(lambda: self.emit_data("email"))

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("+7 (XXX) XXX-XX-XX")
        self.phone_edit.setInputMask("+7 (999) 999-99-99")
        self.phone_edit.textChanged.connect(lambda: self.emit_data("phone"))

        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("г. Москва")
        self.address_edit.textChanged.connect(lambda: self.emit_data("address"))

        # Добавление полей в layout
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel("Адрес:"))
        layout.addWidget(self.address_edit)

        self.setLayout(layout)

    def set_data(self, resume):
        self.resume = resume
        personal_info = resume.personal_info

        self.name_edit.setText(personal_info.get("name", ""))
        self.email_edit.setText(personal_info.get("email", ""))
        self.phone_edit.setText(personal_info.get("phone", ""))
        self.address_edit.setText(personal_info.get("address", ""))

    def emit_data(self, field):
        value = getattr(self, f"{field}_edit").text()
        self.data_changed.emit(field, value)


class EducationForm(QWidget):
    data_changed = pyqtSignal(str, object)

    def __init__(self, resume):
        super().__init__()
        self.resume = resume
        self.init_ui()
        self.set_data(resume)

    def init_ui(self):
        layout = QVBoxLayout()

        # Список образовательных учреждений
        self.education_list = QVBoxLayout()

        # Кнопка добавления нового образования
        self.add_btn = QPushButton("Добавить образование")
        self.add_btn.clicked.connect(self.add_education)

        layout.addLayout(self.education_list)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def set_data(self, resume):
        self.resume = resume
        self.clear_education_list()

        for edu in resume.education:
            self.add_education(edu)

    def clear_education_list(self):
        # Удаляем все виджеты образования
        while self.education_list.count():
            item = self.education_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_education(self, education=None):
        """Добавляет новую форму образования"""
        education_widget = EducationItem(education or Education(
            institution="", degree="", field_of_study="", start_date=date.today()
        ))

        education_widget.data_changed.connect(self.update_education)
        education_widget.delete_requested.connect(self.remove_education)

        self.education_list.addWidget(education_widget)

        # Если это новое образование, добавляем в резюме
        if education is None:
            self.resume.education.append(education_widget.education)
            self.data_changed.emit("education", self.resume.education)

    def remove_education(self, widget):
        """Удаляет образование"""
        if widget in self.resume.education:
            self.resume.education.remove(widget.education)

        self.education_list.removeWidget(widget)
        widget.deleteLater()
        self.data_changed.emit("education", self.resume.education)

    def update_education(self, index, education):
        """Обновляет данные образования"""
        if 0 <= index < len(self.resume.education):
            self.resume.education[index] = education
            self.data_changed.emit("education", self.resume.education)


class EducationItem(QWidget):
    data_changed = pyqtSignal(int, Education)
    delete_requested = pyqtSignal(QWidget)

    def __init__(self, education):
        super().__init__()
        self.education = education
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Поля для ввода данных
        institution_layout = QHBoxLayout()
        institution_layout.addWidget(QLabel("Учебное заведение:"))
        self.institution_edit = QLineEdit()
        self.institution_edit.setText(self.education.institution)
        self.institution_edit.textChanged.connect(self.update_data)
        institution_layout.addWidget(self.institution_edit)

        degree_layout = QHBoxLayout()
        degree_layout.addWidget(QLabel("Степень:"))
        self.degree_edit = QLineEdit()
        self.degree_edit.setText(self.education.degree)
        self.degree_edit.textChanged.connect(self.update_data)
        degree_layout.addWidget(self.degree_edit)

        field_layout = QHBoxLayout()
        field_layout.addWidget(QLabel("Специальность:"))
        self.field_edit = QLineEdit()
        self.field_edit.setText(self.education.field_of_study)
        self.field_edit.textChanged.connect(self.update_data)
        field_layout.addWidget(self.field_edit)

        dates_layout = QHBoxLayout()
        dates_layout.addWidget(QLabel("Начало обучения:"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(self.education.start_date)
        self.start_date_edit.dateChanged.connect(self.update_data)
        dates_layout.addWidget(self.start_date_edit)

        dates_layout.addWidget(QLabel("Окончание:"))
        self.end_date_edit = QDateEdit()
        if self.education.end_date:
            self.end_date_edit.setDate(self.education.end_date)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.dateChanged.connect(self.update_data)
        dates_layout.addWidget(self.end_date_edit)

        # Описание
        self.description_edit = QTextEdit()
        self.description_edit.setPlainText(self.education.description)
        self.description_edit.textChanged.connect(self.update_data)

        # Кнопка удаления
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))

        # Добавление всех виджетов в layout
        layout.addLayout(institution_layout)
        layout.addLayout(degree_layout)
        layout.addLayout(field_layout)
        layout.addLayout(dates_layout)
        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description_edit)
        layout.addWidget(delete_btn)

        self.setLayout(layout)

    def update_data(self):
        """Обновляет данные на основе введенных значений"""
        self.education.institution = self.institution_edit.text()
        self.education.degree = self.degree_edit.text()
        self.education.field_of_study = self.field_edit.text()
        self.education.start_date = self.start_date_edit.date().toPyDate()
        self.education.end_date = self.end_date_edit.date().toPyDate()
        self.education.description = self.description_edit.toPlainText()

        # Эмитируем сигнал с обновленными данными
        self.data_changed.emit(self.get_index(), self.education)

    def get_index(self):
        """Возвращает индекс этого элемента в списке"""
        parent = self.parent()
        if parent:
            for i in range(parent.layout().count()):
                item = parent.layout().itemAt(i)
                if item.widget() == self:
                    return i
        return -1


class SkillsForm(QWidget):
    data_changed = pyqtSignal(str, object)

    def __init__(self, resume):
        super().__init__()
        self.resume = resume
        self.init_ui()
        self.set_data(resume)

    def init_ui(self):
        layout = QVBoxLayout()

        # Список навыков
        self.skills_list = QVBoxLayout()

        # Форма добавления нового навыка
        self.new_skill_layout = QHBoxLayout()

        self.skill_name_edit = QLineEdit()
        self.skill_name_edit.setPlaceholderText("Название навыка")

        self.skill_category_combo = QComboBox()
        self.skill_category_combo.addItems(["Technical", "Soft", "Language", "Other"])

        self.skill_level_spin = QSpinBox()
        self.skill_level_spin.setRange(1, 5)
        self.skill_level_spin.setValue(3)

        self.add_skill_btn = QPushButton("Добавить")
        self.add_skill_btn.clicked.connect(self.add_skill)

        self.new_skill_layout.addWidget(QLabel("Навык:"))
        self.new_skill_layout.addWidget(self.skill_name_edit)
        self.new_skill_layout.addWidget(QLabel("Категория:"))
        self.new_skill_layout.addWidget(self.skill_category_combo)
        self.new_skill_layout.addWidget(QLabel("Уровень (1-5):"))
        self.new_skill_layout.addWidget(self.skill_level_spin)
        self.new_skill_layout.addWidget(self.add_skill_btn)

        layout.addLayout(self.new_skill_layout)
        layout.addLayout(self.skills_list)

        self.setLayout(layout)

    def set_data(self, resume):
        self.resume = resume
        self.clear_skills_list()

        for skill in resume.skills:
            self.add_skill_item(skill)

    def clear_skills_list(self):
        # Удаляем все виджеты навыков
        while self.skills_list.count():
            item = self.skills_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_skill(self):
        """Добавляет новый навык"""
        name = self.skill_name_edit.text().strip()
        if not name:
            return

        category = self.skill_category_combo.currentText()
        level = self.skill_level_spin.value()

        skill = Skill(name=name, level=level, category=category)
        self.resume.skills.append(skill)
        self.add_skill_item(skill)

        # Очищаем поля ввода
        self.skill_name_edit.clear()
        self.skill_level_spin.setValue(3)

        # Обновляем данные
        self.data_changed.emit("skills", self.resume.skills)

    def add_skill_item(self, skill):
        """Добавляет виджет навыка в список"""
        skill_widget = QWidget()
        skill_layout = QHBoxLayout(skill_widget)

        name_label = QLabel(f"{skill.name} ({skill.category})")
        level_label = QLabel("★" * skill.level)

        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(lambda: self.remove_skill(skill, skill_widget))

        skill_layout.addWidget(name_label, 1)
        skill_layout.addWidget(level_label)
        skill_layout.addWidget(delete_btn)

        self.skills_list.addWidget(skill_widget)

    def remove_skill(self, skill, widget):
        """Удаляет навык"""
        if skill in self.resume.skills:
            self.resume.skills.remove(skill)

        self.skills_list.removeWidget(widget)
        widget.deleteLater()
        self.data_changed.emit("skills", self.resume.skills)


class ExperienceForm(QWidget):
    data_changed = pyqtSignal(str, object)

    def __init__(self, resume):
        super().__init__()
        self.resume = resume
        self.init_ui()
        self.set_data(resume)

    def init_ui(self):
        layout = QVBoxLayout()

        # Список мест работы
        self.experience_list = QVBoxLayout()

        # Кнопка добавления нового места работы
        self.add_btn = QPushButton("Добавить место работы")
        self.add_btn.clicked.connect(self.add_experience)

        layout.addLayout(self.experience_list)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def set_data(self, resume):
        self.resume = resume
        self.clear_experience_list()

        for exp in resume.work_experience:
            self.add_experience(exp)

    def clear_experience_list(self):
        # Удаляем все виджеты опыта работы
        while self.experience_list.count():
            item = self.experience_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_experience(self, experience=None):
        """Добавляет новую форму опыта работы"""
        experience_widget = ExperienceItem(experience or WorkExperience(
            company="", position="", start_date=date.today()
        ))

        experience_widget.data_changed.connect(self.update_experience)
        experience_widget.delete_requested.connect(self.remove_experience)

        self.experience_list.addWidget(experience_widget)

        # Если это новое место работы, добавляем в резюме
        if experience is None:
            self.resume.work_experience.append(experience_widget.experience)
            self.data_changed.emit("work_experience", self.resume.work_experience)

    def remove_experience(self, widget):
        """Удаляет место работы"""
        if widget.experience in self.resume.work_experience:
            self.resume.work_experience.remove(widget.experience)

        self.experience_list.removeWidget(widget)
        widget.deleteLater()
        self.data_changed.emit("work_experience", self.resume.work_experience)

    def update_experience(self, index, experience):
        """Обновляет данные места работы"""
        if 0 <= index < len(self.resume.work_experience):
            self.resume.work_experience[index] = experience
            self.data_changed.emit("work_experience", self.resume.work_experience)


class ExperienceItem(QWidget):
    data_changed = pyqtSignal(int, WorkExperience)
    delete_requested = pyqtSignal(QWidget)

    def __init__(self, experience):
        super().__init__()
        self.experience = experience
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Поля для ввода данных
        company_layout = QHBoxLayout()
        company_layout.addWidget(QLabel("Компания:"))
        self.company_edit = QLineEdit()
        self.company_edit.setText(self.experience.company)
        self.company_edit.textChanged.connect(self.update_data)
        company_layout.addWidget(self.company_edit)

        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("Должность:"))
        self.position_edit = QLineEdit()
        self.position_edit.setText(self.experience.position)
        self.position_edit.textChanged.connect(self.update_data)
        position_layout.addWidget(self.position_edit)

        dates_layout = QHBoxLayout()
        dates_layout.addWidget(QLabel("Начало работы:"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(self.experience.start_date)
        self.start_date_edit.dateChanged.connect(self.update_data)
        dates_layout.addWidget(self.start_date_edit)

        dates_layout.addWidget(QLabel("Окончание:"))
        self.end_date_edit = QDateEdit()
        if self.experience.end_date:
            self.end_date_edit.setDate(self.experience.end_date)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.dateChanged.connect(self.update_data)
        dates_layout.addWidget(self.end_date_edit)

        self.current_job_check = QCheckBox("По настоящее время")
        self.current_job_check.stateChanged.connect(self.toggle_current_job)
        dates_layout.addWidget(self.current_job_check)

        # Обязанности
        self.responsibilities_edit = QTextEdit()
        self.responsibilities_edit.setPlainText("\n".join(self.experience.responsibilities))
        self.responsibilities_edit.textChanged.connect(self.update_data)

        # Достижения
        self.achievements_edit = QTextEdit()
        self.achievements_edit.setPlainText("\n".join(self.experience.achievements))
        self.achievements_edit.textChanged.connect(self.update_data)

        # Кнопка удаления
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))

        # Добавление всех виджетов в layout
        layout.addLayout(company_layout)
        layout.addLayout(position_layout)
        layout.addLayout(dates_layout)
        layout.addWidget(QLabel("Обязанности:"))
        layout.addWidget(self.responsibilities_edit)
        layout.addWidget(QLabel("Достижения:"))
        layout.addWidget(self.achievements_edit)
        layout.addWidget(delete_btn)

        self.setLayout(layout)

    def toggle_current_job(self, state):
        """Обработчик для чекбокса 'По настоящее время'"""
        if state == Qt.Checked:
            self.end_date_edit.setEnabled(False)
            self.experience.end_date = None
        else:
            self.end_date_edit.setEnabled(True)
            self.experience.end_date = self.end_date_edit.date().toPyDate()

        self.update_data()

    def update_data(self):
        """Обновляет данные на основе введенных значений"""
        self.experience.company = self.company_edit.text()
        self.experience.position = self.position_edit.text()
        self.experience.start_date = self.start_date_edit.date().toPyDate()

        if not self.current_job_check.isChecked():
            self.experience.end_date = self.end_date_edit.date().toPyDate()

        self.experience.responsibilities = [
            resp.strip() for resp in self.responsibilities_edit.toPlainText().split("\n")
            if resp.strip()
        ]
        self.experience.achievements = [
            ach.strip() for ach in self.achievements_edit.toPlainText().split("\n")
            if ach.strip()
        ]

        # Эмитируем сигнал с обновленными данными
        self.data_changed.emit(self.get_index(), self.experience)

    def get_index(self):
        """Возвращает индекс этого элемента в списке"""
        parent = self.parent()
        if parent:
            for i in range(parent.layout().count()):
                item = parent.layout().itemAt(i)
                if item.widget() == self:
                    return i
        return -1