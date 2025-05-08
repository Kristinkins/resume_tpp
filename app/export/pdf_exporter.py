from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QMarginsF
import os
import tempfile


class PDFExporter:
    @staticmethod
    def export(resume, filename):
        """Экспортирует резюме в PDF файл"""
        # Создаем временный HTML файл
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            html_content = PreviewPanel.generate_html(resume)
            f.write(html_content)
            temp_path = f.name

        # Создаем QWebEngineView для рендеринга HTML
        view = QWebEngineView()
        view.load(QUrl.fromLocalFile(temp_path))

        # Ждем загрузки страницы
        loop = QEventLoop()
        view.loadFinished.connect(loop.quit)
        loop.exec_()

        # Настройка принтера
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        printer.setPageMargins(QMarginsF(10, 10, 10, 10))

        # Печать в PDF
        view.page().print(printer, lambda success: print(f"PDF exported: {success}"))

        # Удаляем временный файл
        os.unlink(temp_path)