from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import QUrl
from ...core.models import Resume
import os


class PreviewPanel(QWidget):
    def __init__(self, resume):
        super().__init__()
        self.resume = resume
        self.init_ui()
        self.update_preview(resume)

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор шаблона
        self.template_combo = QComboBox()
        self.template_combo.addItems(["modern", "classic"])
        self.template_combo.currentTextChanged.connect(self.change_template)

        # Превью резюме
        self.web_view = QTextBrowser()

        layout.addWidget(QLabel("Шаблон:"))
        layout.addWidget(self.template_combo)
        layout.addWidget(self.web_view)

        self.setLayout(layout)

    def update_preview(self, resume):
        """Обновляет превью на основе данных резюме"""
        self.resume = resume

        # Генерируем HTML для текущего шаблона
        html_content = self.generate_html()

        # Отображаем HTML в WebView
        self.web_view.setHtml(html_content)

    def change_template(self, template_name):
        """Меняет шаблон резюме"""
        self.resume.template = template_name
        self.update_preview(self.resume)

    def generate_html(self) -> str:
        """Генерирует HTML для текущего шаблона"""
        template_dir = os.path.join(
            os.path.dirname(__file__), "..", "templates", self.resume.template
        )

        # Загружаем шаблон HTML
        with open(os.path.join(template_dir, "template.html"), "r", encoding="utf-8") as f:
            html_template = f.read()

        # Загружаем CSS стили
        with open(os.path.join(template_dir, "style.css"), "r", encoding="utf-8") as f:
            css_styles = f.read()

        # Заменяем плейсхолдеры на данные резюме
        html_content = html_template.replace("/* CSS_STYLES */", css_styles)

        # Заменяем данные
        html_content = html_content.replace("{{name}}", self.resume.personal_info.get("name", ""))
        html_content = html_content.replace("{{email}}", self.resume.personal_info.get("email", ""))
        html_content = html_content.replace("{{phone}}", self.resume.personal_info.get("phone", ""))

        # Генерация секции опыта работы
        experience_html = ""
        for exp in self.resume.work_experience:
            experience_html += f"""
            <div class="experience-item">
                <h3>{exp.company}</h3>
                <p class="position">{exp.position}</p>
                <p class="date">{utils.format_date_range(exp.start_date, exp.end_date)}</p>
                <ul class="responsibilities">
                    {"".join(f"<li>{resp}</li>" for resp in exp.responsibilities if resp)}
                </ul>
            </div>
            """
        html_content = html_content.replace("{{experience}}", experience_html)

        # Аналогично для образования, навыков и других секций

        return html_content