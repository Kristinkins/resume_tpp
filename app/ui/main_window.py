from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from ..core.resume_manager import ResumeManager
from ..core.models import Resume
from .widgets.form_fields import PersonalInfoForm, ExperienceForm, EducationForm, SkillsForm
from .widgets.preview_panel import PreviewPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resume Builder")
        self.resize(1200, 800)

        self.resume_manager = ResumeManager()
        self.current_resume = self.resume_manager.create_default_resume()

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # Главный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Левая панель - форма ввода
        self.form_tabs = QTabWidget()
        self.personal_info_form = PersonalInfoForm(self.current_resume)
        self.experience_form = ExperienceForm(self.current_resume)
        self.education_form = EducationForm(self.current_resume)
        self.skills_form = SkillsForm(self.current_resume)

        self.form_tabs.addTab(self.personal_info_form, "Личные данные")
        self.form_tabs.addTab(self.experience_form, "Опыт работы")
        self.form_tabs.addTab(self.education_form, "Образование")
        self.form_tabs.addTab(self.skills_form, "Навыки")

        # Правая панель - предпросмотр
        self.preview_panel = PreviewPanel(self.current_resume)

        # Разделение экрана
        main_layout.addWidget(self.form_tabs, 1)
        main_layout.addWidget(self.preview_panel, 1)

        # Панель инструментов
        self.init_toolbar()

    def init_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")

        # Кнопки управления
        self.new_btn = QPushButton("Новое")
        self.open_btn = QPushButton("Открыть")
        self.save_btn = QPushButton("Сохранить")
        self.export_pdf_btn = QPushButton("Экспорт в PDF")
        self.export_docx_btn = QPushButton("Экспорт в DOCX")

        toolbar.addWidget(self.new_btn)
        toolbar.addWidget(self.open_btn)
        toolbar.addWidget(self.save_btn)
        toolbar.addWidget(QLabel("|"))
        toolbar.addWidget(self.export_pdf_btn)
        toolbar.addWidget(self.export_docx_btn)

    def setup_connections(self):
        # Подключение сигналов форм к обновлению резюме
        self.personal_info_form.data_changed.connect(self.update_resume)
        self.experience_form.data_changed.connect(self.update_resume)
        self.education_form.data_changed.connect(self.update_resume)
        self.skills_form.data_changed.connect(self.update_resume)

        # Подключение кнопок
        self.new_btn.clicked.connect(self.new_resume)
        self.open_btn.clicked.connect(self.open_resume)
        self.save_btn.clicked.connect(self.save_resume)
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)
        self.export_docx_btn.clicked.connect(self.export_to_docx)

    def update_resume(self, field: str, value):
        """Обновляет данные резюме и превью"""
        # Обновляем соответствующее поле в резюме
        if hasattr(self.current_resume, field):
            setattr(self.current_resume, field, value)
        elif field in self.current_resume.personal_info:
            self.current_resume.personal_info[field] = value

        # Обновляем превью
        self.preview_panel.update_preview(self.current_resume)

    def new_resume(self):
        """Создает новое резюме"""
        if self.check_unsaved_changes():
            self.current_resume = self.resume_manager.create_default_resume()
            self.reset_forms()
            self.preview_panel.update_preview(self.current_resume)

    def open_resume(self):
        """Открывает существующее резюме"""
        if not self.check_unsaved_changes():
            return

        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть резюме", "data", "JSON Files (*.json)"
        )

        if filename:
            try:
                self.current_resume = self.resume_manager.load_resume(filename)
                self.reset_forms()
                self.preview_panel.update_preview(self.current_resume)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить резюме: {str(e)}")

    def save_resume(self):
        """Сохраняет текущее резюме"""
        try:
            filename = self.resume_manager.save_resume(self.current_resume)
            QMessageBox.information(self, "Сохранено", f"Резюме сохранено в {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить резюме: {str(e)}")

    def export_to_pdf(self):
        """Экспортирует резюме в PDF"""
        # Здесь будет вызов pdf_exporter
        QMessageBox.information(self, "Экспорт", "Экспорт в PDF (заглушка)")

    def export_to_docx(self):
        """Экспортирует резюме в DOCX"""
        # Здесь будет вызов docx_exporter
        QMessageBox.information(self, "Экспорт", "Экспорт в DOCX (заглушка)")

    def check_unsaved_changes(self) -> bool:
        """Проверяет наличие несохраненных изменений"""
        # TODO: Реализовать проверку изменений
        return True

    def reset_forms(self):
        """Сбрасывает все формы к текущему резюме"""
        self.personal_info_form.set_data(self.current_resume)
        self.experience_form.set_data(self.current_resume)
        self.education_form.set_data(self.current_resume)
        self.skills_form.set_data(self.current_resume)

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        if self.check_unsaved_changes():
            event.accept()
        else:
            event.ignore()