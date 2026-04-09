
from typing import Dict
import os
import json
from google import genai
from pydantic import BaseModel
import enum
from dotenv import load_dotenv

load_dotenv()

# Workflow: Prompt Chaining

class Agents:
    
    def __init__(self,api_key: str, model: str, voice_model: str | None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or  os.getenv("CHAT_MODEL")
        self.voice_model = model or  os.getenv("VOICE_MODEL")
        self.client = voice_model or genai.Client(api_key=self.api_key)


    async def agent_validate_resume_jd(self, resume: str, job_description: str) -> bool:
        print("validating resume and job description..")
        """
        Validates input quality and relevance.

        Checks:
        - Resume contains structured career-related content
        - Job description contains role requirements
        - Not empty / garbage / unrelated text

        Returns:
        - True if valid
        - False if invalid
        """
        prompt = f"""
                Resume :{resume}
                Job description:{job_description}
                <role>
                You are a strict grounded resume and job description validation assistant
                limited to resume and job description provided above,
                </role>

                <instructions>
                1. check the resume if its contains structured career-related content
                2. check the Job description if its contains role requirements
                3. confirm is resume and job description  Not empty / garbage / unrelated text
                4. return true if the resume and job description meet number 1 and 2 criteria else return false
                 </instructions>

                 <output_format>
                 strictly return either true or false as python type no additional context
                 </output_format>

                """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text


    async def agent_section_extraction(self, resume: str, job_description: str) -> Dict:
        """
        Extracts structured sections from resume.
        Returns: {
            "summary": str,
            "skills": List[str],
            "experience": List[{
                "title": str,
                "company": str,
                "description": str
            }],
            "education": List[str],
            "projects": List[str]
        }
        """

    async def agent_refinement(self, original_resume: str, extracted_sections: Dict, 
                            job_description: str) -> Dict:
        """
        Improves resume content based on job description.

        Responsibilities:
        - Align experience with JD
        - Enhance bullet points (impact, clarity)
        - Inject missing keywords (without hallucination)
        - Improve structure and phrasing
        -  Generate optimize resume and coverletter

        Returns:
        - optimized resume and coverletter
        """


    async def agent_scoring(self, sections: Dict, job_description: str) -> Dict:
        """
        Computes ATS scores
        - job matching score
        - Keyword
        - skills
        - experience
        - format
        - impact
        """

    async def agent_reflection(self, optimize_resume: str,job_description: str, coverletter: str):
        """
        Evaluates:

        An agent evaluates its own output and uses that feedback to 
        refine its response iteratively

        """
        pass


    async def agent_update_resume_or_coverletter(self):
        """
        conversation agent with tools and memory to update resume or coverletter base on user request
        Tools:
        - tool_update_coverletter
        - tool_update_resume
        - memory
        """