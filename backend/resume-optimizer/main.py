from fastapi import FastAPI, BackgroundTasks,UploadFile,Form,File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from utils.document_processing import ProcessDocument
from ai_services.agents import Agents
from pprint import pprint
import asyncio
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

app = FastAPI(title="Resume Optimizer",
              summary="Advance resume optimization system for ATS (Application Tracking system)")


# CORS (Cross-Origin Resource Sharing) config
origins = [
    "http://localhost:5173/",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/resume/optimize/")
async def optimize_resume(resume:UploadFile,job_description: Annotated[str, Form()]):
    # get the agents class
    agent = Agents(api_key='',model='',voice_model='')
 
    extract_resume_text = ""
    statusError = ""


    # process resume file
    if resume.content_type =="application/pdf":
        logging.info("processing resume: %s type: PDF",resume.filename)
        contents = await resume.read()
        # extract text content from pdf document
        extract_resume_text = ProcessDocument(contents).process_pdf_file() 
    else:
        print(f"processing resume: {resume.filename} type: Docs")
        contents = await resume.read()
         # extract text content from doc document
        extract_resume_text = ProcessDocument(contents).process_docx_file()

    # validate resume and job descriptions
    validated = await agent.agent_validate_resume_jd(extract_resume_text,job_description)


    if validated:
        resume_coverletter_refinement = await agent.agent_refinement(extract_resume_text,job_description)
        if agent.is_error(resume_coverletter_refinement):
              return {"status":"error","message":resume_coverletter_refinement.get('message')}
             
        optimize_resume_coverLetter_reflection = await agent.agent_reflection(resume_coverletter_refinement.resume,job_description,
                                                                   resume_coverletter_refinement.coverletter)
        if agent.is_error(optimize_resume_coverLetter_reflection):
              return {"status":"error","message":optimize_resume_coverLetter_reflection.get('message')}
             

        ats_score = await agent.agent_scoring(optimize_resume_coverLetter_reflection.get('resume'),job_description)

        if agent.is_error(ats_score):
               return {"status":"error","message":ats_score.get('message')}
             
        summary_insight = await agent.insight_agent(resume,optimize_resume_coverLetter_reflection.get('resume'),job_description,ats_score)
        if agent.is_error(summary_insight):
              return {"status":"error","message":summary_insight.get('message')}
        
              
        optimize_result = {
            "optimizeResume":optimize_resume_coverLetter_reflection.get('resume'),
            "coverLetter":optimize_resume_coverLetter_reflection.get('coverletter'),
            "ats_score":ats_score,
            "insight_summary": summary_insight
            }
        return optimize_result

    elif validated.get('status') == "error":          
            return   {"status":"error","message":validated['message']}
    else:
            return {"status":"error","message":"upload a valid resume or job description"}
    
    
    


@app.post("/chat/agent/{optimize_resume}/{coverletter}/{job_description}/{user_query}")
async def chat_agent(optimize_resume: str, coverletter: str,
                        job_description: str, user_query:str ):
     
    return {"documents":""}