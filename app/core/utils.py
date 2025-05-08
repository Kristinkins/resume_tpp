import re
from datetime import date
from typing import Optional


def validate_email(email: str) -> bool:
    """Проверяет корректность email адреса"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Проверяет корректность номера телефона"""
    # Простая проверка для российских номеров
    cleaned = re.sub(r"[^\d+]", "", phone)
    return len(cleaned) >= 10 and cleaned.startswith(("7", "+7", "8"))


def calculate_experience(work_experience: list) -> float:
    """Вычисляет общий стаж работы в годах"""
    total_days = 0

    for job in work_experience:
        end_date = job.end_date if job.end_date else date.today()
        delta = end_date - job.start_date
        total_days += delta.days

    return round(total_days / 365, 1)


def format_date_range(start_date, end_date=None) -> str:
    """Форматирует период в строку вида 'MM.YYYY – MM.YYYY'"""
    start_str = start_date.strftime("%m.%Y")
    end_str = end_date.strftime("%m.%Y") if end_date else "н.в."
    return f"{start_str} – {end_str}"


def generate_filename(name: str, suffix: str = "") -> str:
    """Генерирует имя файла на основе имени"""
    clean_name = re.sub(r"[^\w\s-]", "", name.strip().lower())
    clean_name = re.sub(r"[-\s]+", "_", clean_name)
    return f"{clean_name}{f'_{suffix}' if suffix else ''}"