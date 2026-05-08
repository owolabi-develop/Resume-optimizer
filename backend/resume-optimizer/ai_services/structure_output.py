from pydantic import BaseModel, Field,HttpUrl
from typing import List, Optional
from datetime import date
import enum


class ValidationStatus(BaseModel):
    status:bool


class OptimizeResumeCoverletter(BaseModel):
    resume: str = Field(description="The fully optimized resume written in markdown format")
    coverletter: str = Field(description="The tailored cover letter written in markdown format")


class ATSScore(BaseModel):
    job_matching_score: int  = Field(description="the total matching score of the job")
    keyword: int  = Field(description="the numbers of keyword matching the candidate resume")
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

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MemoryLogs(BaseModel):
    action: Literal[
        "add_skill",
        "remove_skill",
        "update_summary",
        "rewrite_experience",
        "update_cover_letter"
    ] = Field(description="Type of change made by the AI")
    section: str = Field(description="Section of resume that was modified")
    detail: str = Field(description="Short description of what changed and what you did")
    user_intent: str = Field(description="What the user asked for")
    timestamp: datetime = Field(default_factory=datetime.now())




class UpdateResume(BaseModel):
    resume:str
    summary:str = Field(description="Short description of what changed and what you did on the resume")

class UpdateCoverletter(BaseModel):
    coverletter:str
    summary: str = Field(description="Short description of what changed and what you did on the coverletter")


class ChatAgent(BaseModel):
    coverLetter:str
    optimized_resume: str
    job_description:str
    user_query: str
    model_name: str
    model_api_key: str


class ResumeData(BaseModel):
      model_name: str
      model_api_key: str
      job_description: str