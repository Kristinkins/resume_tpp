import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication
from app.ui.main_window import MainWindow
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"


def handle_exception(exc_type, exc_value, exc_traceback):
    """Перехват всех необработанных исключений"""
    from traceback import format_exception
    error_msg = ''.join(format_exception(exc_type, exc_value, exc_traceback))
    print(f"Critical error:\n{error_msg}", file=sys.stderr)
    QCoreApplication.exit(1)


def main():
    # Настройка обработки исключений
    sys.excepthook = handle_exception

    # Настройка переменных окружения для Qt
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

    # Проверка и создание QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Настройки HighDPI
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Установка стиля (опционально)
    try:
        from PyQt5.QtGui import QFont
        font = QFont("Segoe UI", 9)
        app.setFont(font)
        # app.setStyle('Fusion')  # Альтернативный стиль
    except Exception as e:
        print(f"Could not set font/style: {str(e)}")

    try:
        # Создание и отображение главного окна
        window = MainWindow()
        window.show()

        # Запуск основного цикла
        ret = app.exec_()
        sys.exit(ret)

    except Exception as e:
        print(f"Application error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("Starting application...")  # Для отладки
    main()