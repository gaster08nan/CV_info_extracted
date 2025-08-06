from pydantic import BaseModel, EmailStr, ValidationError
from typing import List, Optional

class EducationItem(BaseModel):
    degree: str
    institution: str
    graduation_year: Optional[str]

class ExperienceItem(BaseModel):
    job_title: str
    company_name: str
    years_worked: Optional[str]
    description: Optional[str]

class CVSchema(BaseModel):
    Name: Optional[str]
    Email: Optional[EmailStr]
    Phone: Optional[str]
    Skills: List[str]
    Education: List[EducationItem]
    Experience: Optional[List[ExperienceItem]]
    Certification: Optional[List[str]]
    Languages: Optional[List[str]]
