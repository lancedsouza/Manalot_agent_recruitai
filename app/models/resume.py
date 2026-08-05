# app/models/resume.py

from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str

class Experience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: str

class Resume(BaseModel):
    name: str
    skills: list[str]
    experience_years: float
    education: list[Education]
    experience: list[Experience]
    projects: list[str]