from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class Education:
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None
    description: str = ""


@dataclass
class WorkExperience:
    company: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    responsibilities: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)


@dataclass
class Skill:
    name: str
    level: int  # 1-5
    category: str = "Other"


@dataclass
class Resume:
    personal_info: dict = field(default_factory=dict)
    education: List[Education] = field(default_factory=list)
    work_experience: List[WorkExperience] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    languages: List[dict] = field(default_factory=list)
    projects: List[dict] = field(default_factory=list)
    certifications: List[dict] = field(default_factory=list)
    template: str = "modern"

    def to_dict(self):
        # Преобразуем объект в словарь для сериализации
        return {
            "personal_info": self.personal_info,
            "education": [{
                "institution": edu.institution,
                "degree": edu.degree,
                "field_of_study": edu.field_of_study,
                "start_date": edu.start_date.isoformat(),
                "end_date": edu.end_date.isoformat() if edu.end_date else None,
                "description": edu.description
            } for edu in self.education],
            "work_experience": [{
                "company": exp.company,
                "position": exp.position,
                "start_date": exp.start_date.isoformat(),
                "end_date": exp.end_date.isoformat() if exp.end_date else None,
                "responsibilities": exp.responsibilities,
                "achievements": exp.achievements
            } for exp in self.work_experience],
            "skills": [{
                "name": skill.name,
                "level": skill.level,
                "category": skill.category
            } for skill in self.skills],
            "languages": self.languages,
            "projects": self.projects,
            "certifications": self.certifications,
            "template": self.template
        }

    @classmethod
    def from_dict(cls, data):
        # Создаем объект Resume из словаря
        resume = cls()
        resume.personal_info = data.get("personal_info", {})

        # Обработка образования
        for edu_data in data.get("education", []):
            education = Education(
                institution=edu_data["institution"],
                degree=edu_data["degree"],
                field_of_study=edu_data["field_of_study"],
                start_date=date.fromisoformat(edu_data["start_date"]),
                end_date=date.fromisoformat(edu_data["end_date"]) if edu_data["end_date"] else None,
                description=edu_data.get("description", "")
            )
            resume.education.append(education)

        # Обработка опыта работы
        for exp_data in data.get("work_experience", []):
            experience = WorkExperience(
                company=exp_data["company"],
                position=exp_data["position"],
                start_date=date.fromisoformat(exp_data["start_date"]),
                end_date=date.fromisoformat(exp_data["end_date"]) if exp_data["end_date"] else None,
                responsibilities=exp_data.get("responsibilities", []),
                achievements=exp_data.get("achievements", [])
            )
            resume.work_experience.append(experience)

        # Обработка навыков
        for skill_data in data.get("skills", []):
            skill = Skill(
                name=skill_data["name"],
                level=skill_data["level"],
                category=skill_data.get("category", "Other")
            )
            resume.skills.append(skill)

        resume.languages = data.get("languages", [])
        resume.projects = data.get("projects", [])
        resume.certifications = data.get("certifications", [])
        resume.template = data.get("template", "modern")

        return resume