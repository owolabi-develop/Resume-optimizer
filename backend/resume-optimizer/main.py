from fastapi import FastAPI, BackgroundTasks,UploadFile,Form,File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from utils.document_processing import ProcessDocument
from ai_services.agents import Agents
from pprint import pprint
import asyncio

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

    # process resume file
    if resume.content_type =="application/pdf":
        print(f"processing resume: {resume.filename} type: PDF")
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
        optimize_resume_coverLetter = await agent.agent_reflection(resume_coverletter_refinement.resume,job_description,
                                                                   resume_coverletter_refinement.coverletter)

        ats_score = await agent.agent_scoring(optimize_resume_coverLetter['resume'],job_description)
        summary_insight = await agent.insight_agent(resume,optimize_resume_coverLetter['resume'],job_description,ats_score)
        optimize_result = {
            "optimizeResume":optimize_resume_coverLetter['resume'],
            "coverLetter":optimize_resume_coverLetter['coverletter'],
            "ats_score":ats_score,
            "insight_summary": summary_insight
        }
        optimize_resume = optimize_resume_coverLetter['resume']
        pprint(optimize_resume_coverLetter,indent=4)
        return optimize_result 
         
    else:
        return {"status":"Error"}
    


@app.post("/chat/agent/")
async def chat_agent(optimize_resume: str, coverletter: str,
                        job_description: str, user_query:str ):
     
    return {"documents":""}