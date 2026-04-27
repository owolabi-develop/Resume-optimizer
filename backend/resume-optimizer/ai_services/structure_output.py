from pydantic import BaseModel, Field,HttpUrl
from typing import List, Optional
from datetime import date
import enum


class ValidationStatus(BaseModel):
    status:bool


class OptimizeResumeCoverletter(BaseModel):
    resume: str = Field(description="the optimize resume text return as markdown")
    coverletter: str = Field(description="the optimize coverletter text return as markdown")


class ATSScore(BaseModel):
    job_matching_score: int  = Field(description="the total matching score of the job")
    Keyword: int  = Field(description="the numbers of keyword matching the candidate resume")
    skills: int  = Field(description="The numbers of skill match on the candidate resume ")
    experience: int  = Field(description="The candidate experience percentage match the job description")
    impact: int  = Field(description="the impact of the resume")
    



class EvaluationStatus(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class OptimizeResumeEvaluation(BaseModel):
    evaluation: EvaluationStatus
    feedback: str
    reasoning: str

class Category(enum.Enum):
    RESUME = "resume"
    COVERLETTER = "coverletter"
    UNKNOWN = "unknown"
 
class RoutingDecision(BaseModel):
    category: Category
    reasoning: str