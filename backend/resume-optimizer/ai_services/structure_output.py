from pydantic import BaseModel, Field,HttpUrl
from typing import List, Optional
from datetime import date
import enum


class ValidationStatus(BaseModel):
    status:bool

class Skill(BaseModel):
    technical_skills: List[str] = Field(description="list of technical skill of the candidate")
    soft_skill: Optional[List[str]] = Field(description="list of soft skill  of the candidate")


class Certifications(BaseModel):
    name: str = Field(description="Organization Name of certification")
    start_date: Optional[date] = Field(description="start date of learning")
    end_date: Optional[date] = Field(description="end date of the learning")

class Education(BaseModel):
    university_name: str = Field(description="Name of university")
    degree: str =  Field(description="degree obtain")
    gpa: Optional[float] = Field(gt=0,le=10.0, description="GPA (0-10 scale)")

class Experience(BaseModel):
    company_name: str = Field(description="Name of the company")
    role: Optional[str]  = Field(description="Role position at the company")
    employment_type: Optional[str]  = Field(description="employment type full-time, part-time,contract")
    project_description: Optional[List[str]]  = Field(description="Role and achievement describe in the project")
    tech_stack: Optional[str]  = Field(description="Technology and tools use in the project")
    start_date: Optional[date] = Field(description="start date of learning")
    location: str = Field(description="city/state of the company, remote,onsite,hybrid")
    end_date: Optional[date] = Field(description="end date of the learning")


class ResumeData(BaseModel):
    title: str = Field(description="title of the candidate")
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email Address of the candidate")
    phoneNumber: str = Field(description="Phone number of the candidate")
    linkedInURL: Optional[str] = Field(description="LinkedIn URL of the candidate")
    github: Optional[HttpUrl] =  Field(description="Candidate github address")
    skills: Skill
    summary: str = Field(description="Professional summary  of the candidate")
    objective: Optional[str] = Field(description="Career objective of the candidate")
    experience: Optional[List[Experience]] = Field(description="List of professional experience")
    education: Optional[List[Education]] = Field(description="List of educational background")
    certifications: Optional[List[Certifications]] = Field(description="List of certifications obtain")


class OptimizeResumeCoverletter(BaseModel):
    resume: str = Field(description="the optimize resume text return as markdown")
    coverletter: str = Field(description="the optimize coverletter text return as markdown")


class ATSScore(BaseModel):
    job_matching_score: int  = Field(description="the total matching score of the job")
    Keyword: int  = Field(description="the numbers of keyword matching the candidate resume")
    skills: int  = Field(description="The numbers of skill match on the candidate resume ")
    experience: int  = Field(description="The candidate experience percentage match the job description")
    format:int  = Field(description="Ats resume format return percentage ")
    impact: int  = Field(description="the impact of the resume")



class EvaluationStatus(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class OptimizeResumeEvaluation(BaseModel):
    evaluation: EvaluationStatus
    feedback: str
    reasoning: str