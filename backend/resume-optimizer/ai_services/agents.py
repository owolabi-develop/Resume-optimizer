
from typing import Dict
import os
import json
from google import genai
from google.genai import errors
import logging
import asyncio
from dotenv import load_dotenv
from .structure_output import (ValidationStatus,OptimizeResumeCoverletter,OptimizeResumeEvaluation,
                               EvaluationStatus,ATSScore,RoutingDecision,Category,UpdateCoverletter,UpdateResume)
load_dotenv()
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)


# Workflow: Prompt Chaining



class Agents:
    
    def __init__(self,api_key: str, model: str, voice_model: str | None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or  os.getenv("CHAT_MODEL")
        self.voice_model = model or  os.getenv("VOICE_MODEL")
        self.client = voice_model or genai.Client(api_key=self.api_key)
    
    def is_error(self,result) -> bool:
        return isinstance(result,dict) and result.get('status') == "error"


    async def agent_validate_resume_jd(self, resume: str, job_description: str) -> bool:
        logging.info("validating resume and job description..")
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

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
            "response_mime_type": "application/json",
            "response_json_schema": ValidationStatus.model_json_schema()},
            )
            result = ValidationStatus.model_validate_json(response.text)
           
        except (errors.APIError, errors.ServerError,errors.ClientError) as e:   
            logging.error('%s',str(e.message))
            return {"status":"error","message":str(e.message)[0:100]}
        else:
            return result.status 


    

    async def agent_refinement(self, extracted_resume_sections: Dict, 
                            job_description: str) -> Dict:
        logging.info("refining resume and job descriptions")
        
        prompt = f"""
    
                 <role> 
                You are an expert ATS resume and cover letter optimization assistant.
                Your goal is to optimized the resume strictly based on the candidate’s actual experience.
                 </role>

                 <context>
                  RESUME DATA:
                  {extracted_resume_sections}

                  JOB DESCRIPTION: 
                  {job_description}
                 </context>

                 <instructions>
                    RESUME OPTIMIZATION RULE:
                    1. Align the candidate’s title with the job title where appropriate
                    2. Based on the the job description rewrite the objective and professional summary to clearly match the role
                    3. include job-specific keywords from the job description to ensure the resume matches the job requirements.
                    4. Turn the candidate responsibilities into measurable achievement
                    5. carefully refine the candidate most recent and relevant roles working experience, and cutout any ambiguous
                    key achievement, task carried out not relating to their responsibilities that doesn't add any value. then 
                    6. Strictly rewrite each role working experience of the candidate with bullet points that features the keywords and skill found on the job description.
                    7. For each role craft a bullet point that tells a story of impact and result driven.
                    8. Strictly avoid adding any details to the optimize resume not included on the job description

                    RESUME DESIGN FORMAT RULES:
                    <header>
                    - Candidate name must be on the first line in uppercase and center of the document
                    - Job title on the second line
                    - Phone third line (if available)
                    - Email forth line (if available)
                    - LinkedIn fifth line (if available)
                    - Portfolio sixth line (if available)
                    - Github seventh line (if available)
                    
                    - all inside the header section
                    </header>
                    - Use a standard single-column layout
                    - Use clear section header: Summary, Skills, Experience, Projects, Education, Certifications (if available).
                    - Each section header should be h1:
                        - Be in UPPERCASE
                        - Be bold
                        - End with a colon (e.g., **EXPERIENCE:**, **SKILLS:**)
                    - Use simple formatting with proper spacing and consistent structure.
                    - Avoid special characters, icons, emojis, or complex formatting.
                    - add horizontal line where appropriate
    
                    

                    EXPERIENCE SECTION RULES:
                    Job Title | Company Name | Location | Date
                    - Focus on achievements, not responsibilities
                    BULLET POINT RULES:
                    - All responsibilities and achievements must be written as markdown unordered list
                    - Start with a strong action verb

                    EXPERIENCE SECTION MARKDOWN FORMAT DESIGN RULE EXAMPLE:
                    **Growth Associate | Company Pvt. Ltd. (P2P, O2C, AP/AR Systems)** | *Oct 2025 – Dec 2025*
                    * Structured more than 50 enterprise dataset files containing vendor masters, customer registries, and product inventories through spreadsheet normalization, validation routines, 
                        
                    SKILLS SECTION RULES:
                    - Group skills into categories of an unordered list:
                    - Programming Languages
                    - Frameworks & Tools
                    - Cloud & DevOps
                    - Databases
                    - Avoid long paragraphs—use clean lists 
                
                    COVER LETTER GENERATION RULE:
                    - Write a concise and tailored cover letter
                    - Clearly connect candidate experience to job requirements
                    - Show alignment with company goals
                    - Keep it professional and direct

                    COVERLETTER STRUCTURE:
                    - Use a standard business format:
                    - Greeting (e.g., "Dear Hiring Manager,")
                    - Opening paragraph
                    - Closing paragraph
                    - Professional sign-off (e.g., "Sincerely,")

                    OUTPUT RULES:
                    - Return both the final formatted resume and coverletter
                    - Do NOT include explanations
                    - Use clean markdown formatting
                    - Ensure readability and professional tone
                    
                 
                 </instructions> 

                 <output_format>
                  return a clean markdown format for both optimized resume and the coverletter 
                </output_format>
                
                 Strictly follow all the resume and coverletter design format rules:
                 """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
            "response_mime_type": "application/json",
            "response_json_schema": OptimizeResumeCoverletter.model_json_schema()},
            )
            resume_coverletter = OptimizeResumeCoverletter.model_validate_json(response.text)
        except (errors.APIError, errors.ServerError, errors.ClientError) as e:   
            logging.error('%s',str(e.message))
            return {"status":"error","message":str(e.message)[0:100]}
        else:
            return resume_coverletter
    
    
    
    

            

    async def agent_reflection(self, optimize_resume: str,job_description: str, coverletter: str):
        logging.info("critiquing the initial output against the requirements or desired quality")

        """
        Evaluates:

        An agent evaluates its own output and uses that feedback to 
        refine its response iteratively

        """
        prompt = f"""

       <role>
       You are resume and coverletter Critique assistant
       </role>
       

       <Context>
       optimize_resume: {optimize_resume}
       job_description: {job_description}
       coverletter: {coverletter}
       </Context>

       <instructions>
        Critique the following optimize_resume and coverletter base on the job description. 
        1. check the optimize resume if the candidate title is align with the exact job description title requirement
        2. check the optimize resume if it's include job-specific keywords from the job description 
        3. check if the optimize resume include Standard clear Headings like "Work Experience Or Experience," 
        "Education," "Skills or Technical Skills" "Professional Summary or Summary", "Projects". 
        4. check each role and working experience of the optimize resume if it's include bullet points 
           that features the keywords and skill identify on the job description not keyword stuffing
        5. check the professional summary and objective statement if it's clearly communicates the 
        candidate goals and alignment with the (JOB TITLE) role at the (COMPANY). Base on the job description
       
       </instructions>

        <output_format>
        Respond with PASS or FAIL and provide feedback.
        </output_format>
       """ 
      #Reflection Loop
        max_iterations = 3
        current_iteration = 0
        optimize_resume_coverletter = ''

        while current_iteration < max_iterations:
            current_iteration +=1

            try:
                response_critique = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={"response_mime_type": "application/json",
                        "response_schema": OptimizeResumeEvaluation}
                        )
            except (errors.APIError, errors.ServerError,errors.ClientError) as e:   
                logging.error('%s',str(e.message))
                return {"status":"error","message":str(e.message)[0:100]}
        
            evaluation_result = response_critique.parsed
            if evaluation_result.evaluation == EvaluationStatus.PASS:
                optimize_resume_coverletter = {
                    "resume":optimize_resume,
                    "coverletter":coverletter
                }
                break
            else:
                result  = await self.agent_refinement(optimize_resume,job_description)
                optimize_resume_coverletter = {
                    "resume":result.resume,
                    "coverletter":result.coverletter
                }
                if current_iteration == max_iterations: 
                  
                  
                  optimize_resume_coverletter = {
                    "resume":optimize_resume,
                    "coverletter":coverletter
                }
                break
        return optimize_resume_coverletter
            
    async def agent_scoring(self, optimizer_resume: str, job_description: str) -> Dict:
        logging.info("Scoring resume and evaluating how well a resume matches a job description.")
        """
        Computes ATS scores
        - job matching score
        - Keyword
        - skills
        - experience
        - impact
        """
        prompt = f"""
                <role>
                You are a strict ATS (Applicant Tracking System) resume scoring assistant.
                Your task is to evaluate how well a resume matches a job description.
                </role>

                <context>
                RESUME:
                {optimizer_resume}

                JOB DESCRIPTION:
                {job_description}
                </context>

                <instructions>

                GENERAL RULES:
                - Do NOT assume missing information
                - Do NOT invent experience or skills
                - Base all scoring strictly on the provided resume content

                SCORING CRITERIA (0–100 each):
                1. KEYWORDS:
                - Compare job description keywords with resume
                - Score based on coverage and relevance

                2. SKILLS:
                - Match required vs present skills
                - Consider depth and relevance

                3. EXPERIENCE:
                - Estimate total years of relevant experience from dates (sum durations, do NOT multiply)
                - Compare with job requirements if provided
                - Evaluate relevance of past roles

                4. IMPACT:
                - Check for measurable achievements (metrics, results, outcomes)
                - Penalize vague or generic responsibilities

                FINAL SCORE:
                - Compute overall job matching score as weighted average:
                    Keywords (30%)
                    Skills (25%)
                    Experience (25%)
                    Impact (20%)
                </instructions>

                <output_format>
                - overall_score
                - keywords
                - skills
                - experience
                - impact

                </output_format>
                """
        try:    
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
            "response_mime_type": "application/json",
            "response_json_schema": ATSScore.model_json_schema()},
            )
            matching_score_details = ATSScore.model_validate_json(response.text).model_dump()

        except (errors.APIError, errors.ServerError, errors.ClientError) as e:   
            logging.error('%s',str(e.message))
            return {"status":"error","message":str(e.message)[0:100]}
        
        return matching_score_details
        

    async def insight_agent(self,original_resume: str, optimized_resume: str, job_description: str, ats_job_score: Dict):
        logging.info("Explaining ATS scoring results clearly and actionably")

        prompt = f"""
                <role>
                You are an AI resume coach that explains ATS scoring results clearly and actionably.
                </role>

                <context>
                ORIGINAL RESUME:
                {original_resume}

                OPTIMIZED RESUME:
                {optimized_resume}

                JOB DESCRIPTION:
                {job_description}

                SCORES:
                {ats_job_score}
                </context>

                <instructions>

                1. Compare original vs optimized resume
                2. Identify what changed and why
                3. Highlight improvements made
                4. Explain remaining gaps
                5. Provide actionable recommendations that the candidate would take to make the resume more align

                Rules:
                - Do NOT repeat entire resume
                - Be specific and concise
                - Focus on improvements and impact
                - strictly don't include any summary

                </instructions>

                <output_format>

                Return markdown format:
                - What Changed
                - Key Improvements
                - Remaining Gaps
                - Actionable Recommendations
                </output_format>
                """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
                )
        except (errors.APIError, errors.ServerError, errors.ClientError) as e:   
            logging.error('%s',str(e.message))
            return {"status":"error","message":str(e.message)[0:100]}
        return response.text


    
    

    async def agent_update_resume_or_coverletter(self,optimize_resume: str, coverletter: str,
                                                  job_description: str, user_query:str ):
        """
        conversation agent with router and memory to update resume or coverletter base on user request
        route:
        - tool_update_coverletter
        - tool_update_resume
        - memory
        """

        prompt_router = f"""
                Analyze the user query below and determine its category.
                Categories:
                - resume: For update or rewrite about the optimize resume.
                - coverletter: For update or rewrite about the coverletter
                - unknown: If the category is unclear.

                Query: {user_query}
              """
        try:
            response_router = self.client.models.generate_content(
                model=self.model,
                contents=prompt_router,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': RoutingDecision,
                },
            )
        except (errors.APIError, errors.ServerError, errors.ClientError) as e: 
                logging.error('%s',str(e.message))
                return {"status":"error","message":str(e.message)[0:100]}

        final_response = ''

        if response_router.parsed.category == Category.RESUME:

            prompt_resume = f"""
                 <role>
               your are a professional resume update assistant. you will be provided an already optimized resume 
               </role>
               <context>
               OPTIMIZED RESUME:
                {optimize_resume}
    
                Query:
                {user_query}
               </context>

                <instructions>
                RULE:
                 - update the candidate resume base on their request
                 - avoid making any changes on the resume which are not requested my the candidate
                 - keep the resume professional as is, aside from the candidate update request 

                 Follow these strict resume design rules:

                    RESUME OPTIMIZATION RULE:
                    1. Align the candidate’s title with the job title where appropriate
                    2. Based on the the job description rewrite the objective and professional summary to clearly match the role
                    3. include job-specific keywords from the job description to ensure the resume matches the job requirements.
                    4. Turn the candidate responsibilities into measurable achievement
                    5. carefully refine the candidate most recent and relevant roles working experience, and cutout any ambiguous
                    key achievement, task carried out not relating to their responsibilities that doesn't add any value. then 
                    6. Strictly rewrite each role working experience of the candidate with bullet points that features the keywords and skill found on the job description.
                    7. For each role craft a bullet point that tells a story of impact and result driven.
                    8. Strictly avoid adding any details to the optimize resume not included on the job description

                    RESUME DESIGN FORMAT RULES:
                    <header>
                    - Candidate name must be on the first line in uppercase and center of the document
                    - Job title on the second line
                    - Contact details on separate lines and well formatted line by line
                    - Job title on the second line
                    - Phone third line (if available)
                    - Email forth line (if available)
                    - LinkedIn fifth line (if available)
                    - Portfolio sixth line (if available)
                    - Github seventh line (if available)
                    - all inside the header section
                    </header>
                    - Use a standard single-column layout
                    - Use clear section header: Summary, Skills, Experience, Projects, Education, Certifications (if available).
                    - Each section header should be h1:
                        - Be in UPPERCASE
                        - Be bold
                        - End with a colon (e.g., **EXPERIENCE:**, **SKILLS:**)
                    - Use simple formatting with proper spacing and consistent structure.
                    - Avoid special characters, icons, emojis, or complex formatting.
                    - add horizontal line where appropriate
    
                    

                    EXPERIENCE SECTION RULES:
                    Job Title | Company Name | Location | Date
                    - Focus on achievements, not responsibilities
                    BULLET POINT RULES:
                    - All responsibilities and achievements must be written as markdown unordered list
                    - Start with a strong action verb

                    EXPERIENCE EXAMPLE FORMAT:
                    **Full Stack Python Developer | Zander Estimate (Remote) | March 2025 – August 2025
                    * Implemented Google OCR to extract and interpret handwritten notes from inspection documents
                
                    SKILLS SECTION RULES:
                    - Group skills into categories of an unordered list:
                    - Programming Languages
                    - Frameworks & Tools
                    - Cloud & DevOps
                    - Databases
                    - Avoid long paragraphs—use clean lists 
                
                    COVER LETTER GENERATION RULE:
                    - Write a concise and tailored cover letter
                    - Clearly connect candidate experience to job requirements
                    - Show alignment with company goals
                    - Keep it professional and direct
                 
                </instructions>

                <output_format>
                return a markdown format of the update resume
                </output_format>
                
                 Strictly follow all the resume design format rules:
                """
            try:
                resume_response =  self.client.models.generate_content(
                    model=self.model,
                    contents=prompt_resume,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": UpdateResume.model_json_schema()
                    },
                )
                updated_resume = UpdateResume.model_validate_json(resume_response.text).model_dump()
            except (errors.APIError, errors.ServerError, errors.ClientError) as e: 
                logging.error('%s',str(e.message))
                return {"status":"error","message":str(e.message)[0:100]}
            
            
            
            async with asyncio.TaskGroup() as tg:
                 new_score = tg.create_task(self.agent_scoring(updated_resume,job_description))
                 new_insight = tg.create_task(self.insight_agent(updated_resume,updated_resume,job_description,new_score))

            final_response = {"type":"resume",
                              "resume":updated_resume.get('resume'),
                               "ats_score":new_score.result(),
                                "insight_summary": new_insight.result(),
                                "agent_summary":updated_resume.get('summary')}
            
        elif response_router.parsed.category == Category.COVERLETTER:
             
            prompt_coverletter = f"""
               <role>
               your are a professional coverletter refiner and update assistant.
               </role>
               <context>
                COVERLETTER:
                {coverletter}

                JOB DESCRIPTION:
                {job_description}

                Query:{user_query}
               </context>

                <instructions>
                1. update the candidate coverletter base on the user request

                COVER LETTER REGENERATION:
                   COVER LETTER GENERATION RULE:
                    - Write a concise and tailored cover letter
                    - Clearly connect candidate experience to job requirements
                    - Show alignment with company goals
                    - Keep it professional and direct

                    COVERLETTER STRUCTURE:
                    - Use a standard business format:
                    - Greeting (e.g., "Dear Hiring Manager,")
                    - Opening paragraph
                    - Closing paragraph
                    - Professional sign-off (e.g., "Sincerely,")
                </instructions>

                <output_format>
                return a markdown format of the update coverletter
                </output_format>
                
                 Strictly follow all the coverletter design format rules:
                """
            try:
                coverletter_response = self.client.models.generate_content(
                    model= self.model,
                    contents=prompt_coverletter,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": UpdateCoverletter.model_json_schema()
                    },
                    )
                updated_coverletter = UpdateCoverletter.model_validate_json(coverletter_response.text).model_dump()
            except (errors.APIError, errors.ServerError, errors.ClientError) as e: 
                logging.error('%s',str(e.message))
                return {"status":"error","message":str(e.message)[0:100]}
            ## update memory with coverletter user intent
            final_response = {"type":"coverLetter","coverLetter":updated_coverletter.get("coverletter"), 
            "agent_summary":updated_coverletter.get('summary')}
        else:
            prompt_unknown = f"""
                    <role>
                    you are a professional response assistant base on the user query
                    </role>
                  

                    <context>
                      The user query is: {prompt_router}
                      Here is the reasoning: {response_router.parsed.reasoning}. 
                      why the candidate query couldn't be answered 
                    </context>

                    <instruction>
                     1. base on the reasoning why the candidate intent could'nt be answered, write a professional response 
                     to the candidate why their request couldn't be answer. Or response to them in a professional manner
                    </instruction>

                    """
            try:
                unknown_response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt_unknown
                    )
            except (errors.APIError, errors.ServerError, errors.ClientError) as e: 
                logging.error('%s',str(e.message))
                return {"status":"error","message":str(e.message)[0:100]}
            final_response = {"type":"unknown","unknown":unknown_response.text}
        return final_response 
