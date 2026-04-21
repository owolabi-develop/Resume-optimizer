
from typing import Dict
import os
import json
from google import genai
import enum
from dotenv import load_dotenv


from .structure_output import ValidationStatus,ResumeData



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
            contents=prompt,
            config={
        "response_mime_type": "application/json",
        "response_json_schema": ValidationStatus.model_json_schema()},
        )
        result = ValidationStatus.model_validate_json(response.text)
        return result.status


    async def agent_sections_extractor(self, resume: str) -> Dict:
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


        prompt = f"""
               <context>
                Resume :{resume}
               </context>
               
                 <role>
                  You are a strict grounded resume extraction sections parsing assistant
                  limited to the resume provided above.
                 </role>

                 <instructions>
                 read through the whole resume document to extract relevant sections
                 1. Extract the candidate details such as
                  - title,
                  - firstName, 
                  - lastName, 
                  - emailAddress.
                  - phoneNumber
                  - professional summary
                  - career objective

                 2. for the candidate skill, extract both technical and soft skill given that technical skill will always be available
                 3. for the candidate experience, extract the 
                   - company name
                   - role position held at the company example (Senior,Junior,lead,Principle etc.)
                   - project descriptions
                   - tech stacks
                   - employment type full-time, part-time,contract
                   - location such as city/state of the company, remote,onsite,hybrid
                   - startDate and endDate
                4. for the candidate education extract the university or college name include their gpa if available
                5. extract the candidate certifications details
                6. job_keywords
                   - extract all relevant tools and specific keyword from the job description

                Note:
                    There will be some resume sample where you will find core competence section, is the same as skill
            
                  </instructions>

                <output_format>
                 strictly return a json schema representation of the sections extracted
                </output_format>
               
                
               """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
        "response_mime_type": "application/json",
        "response_json_schema": ResumeData.model_json_schema()},
        )
        result = ResumeData.model_validate_json(response.text).model_dump()
        return result

    async def agent_refinement(self, extracted_resume_sections: Dict, 
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
        prompt = f"""
    
                 <role> 
                 you are a strict resume and cover optimization assistant limited the 
                 extracted resume sections provide below on the context section.  
                 </role>

                 <context>
                  extracted resume sections :{extracted_resume_sections}
                  job description: {job_description}
                 </context>

                 <instructions>
                  Responsibilities:
                  use the extracted resume sections and job description to generate an optimize resume and coverletter.

                Resume Refinement:
                    1.  Align the candidate title to the exact job description title requirement.
                    2. Craft a Compelling Objective and professional summary Statement  
                    - Based on the the job description, create an objective and professional summary statement that clearly 
                    communicates the candidate goals and alignment with the (JOB TITLE) role at (COMPANY).

                    3. include job-specific keywords from the job description to ensure the resume matches the job requirements.

                    4. Use Standard clear Headings: 
                    - Stick to common headings like "Work Experience Or Experience," "Education," "Skills or Technical Skills"
                    "Professional Summary or Summary", "Projects".

                    5. Ensure there’s a clear hierarchy! 

                    6.  Turn the candidate responsibilities into measurable achievement
                   
                    7. carefully refine the candidate most recent and relevant roles working experience, and cutout any ambiguous
                      key achievement, task carried out not relating to their responsibilities that doesn't add any value. then 
                      highlight each position with bullet points that features the keywords and skill identify on the job description not keyword stuffing, 
                      then for each role craft a bullet point that tells a story of impact and result driven.

                    10. strictly avoid adding any fake or random 

                    11 . Fixed formatting:
                        - use 11 - 12 font size
                        - use professional fonts (Calibri)
                        - use a standard text alignment
                        - return a clean single column structure.
                        - return concise, one page, clean layout, ATS-friendly format.
                        -  Avoid table and text boxes, no design errors.
                        - keep margins clean

                    -  Generate optimize resume and coverletter
                 
                 </instructions>

                 <output_format>
                 strictly return markdown format for both resume and coverletter
                </output_format>

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