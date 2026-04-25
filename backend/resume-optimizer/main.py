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
        extracted_section = await agent.agent_sections_extractor(extract_resume_text)
        resume_coverletter_refinement = await agent.agent_refinement(extracted_section,job_description)
        optimize_resume_coverLetter = await agent.agent_reflection(resume_coverletter_refinement.resume,job_description,
                                                                   resume_coverletter_refinement.coverletter)
        pprint(optimize_resume_coverLetter,indent=4)
    else:
        return {"status":"Error"}
    
    return {"filename":resume.file}


@app.post("/chat/agent/")
async def chat_agent(resume):
    return {"documents":""}