import json
from pathlib import Path
from typing import Optional
from .models import Resume


class ResumeManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_resume(self, resume: Resume, filename: Optional[str] = None) -> str:
        """Сохраняет резюме в JSON файл"""
        if not filename:
            filename = self._generate_filename(resume)

        filepath = self.data_dir / f"{filename}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(resume.to_dict(), f, indent=2, ensure_ascii=False)

        return str(filepath)

    def load_resume(self, filename: str) -> Resume:
        """Загружает резюме из JSON файла"""
        filepath = self.data_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Resume file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Resume.from_dict(data)

    def _generate_filename(self, resume: Resume) -> str:
        """Генерирует имя файла на основе данных резюме"""
        name = resume.personal_info.get("name", "unknown").lower().replace(" ", "_")
        return f"resume_{name}"

    def get_all_resumes(self) -> list:
        """Возвращает список всех сохраненных резюме"""
        return [f.name for f in self.data_dir.glob("*.json")]

    def create_default_resume(self) -> Resume:
        """Создает новое резюме с шаблонными данными"""
        # Можно загружать из default_resume.json
        resume = Resume()
        resume.personal_info = {
            "name": "",
            "email": "",
            "phone": "",
            "address": "",
            "linkedin": "",
            "github": ""
        }
        return resume