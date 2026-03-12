from fastapi import FastAPI, BackgroundTasks,UploadFile,Form,File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from utils.document_processing import ProcessDocument

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
    # process resume file
    if resume.content_type =="application/pdf":
        print(f"processing resume: {resume.filename} type: PDF")
        contents = await resume.read()
        # extract text content from pdf document
        extract_text = ProcessDocument(contents).process_pdf_file()
        
    else:
        print(f"processing resume: {resume.filename} type: Docs")
        contents = await resume.read()
         # extract text content from doc document
        extract_text = ProcessDocument(contents).process_docx_file()
    
    return {"filename":resume.file}


@app.post("/chat/agent/")
async def chat_agent(resume):
    return {"documents":""}