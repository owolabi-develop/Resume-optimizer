## Advanced AI Resume Optimization ATS System

This system allows users to upload their resume (PDF or Word document) along with the job description they are applying for. The application processes the uploaded document, detects the file type, and extracts the text content.

The extracted content is then passed to a Large Language Model (LLM), which analyzes the resume and structures it into meaningful sections.

### Extracted Resume Sections

The system identifies and organizes the resume into the following sections:

- Skills
- Experience
- Education
- Projects
- Professional Summary

This structured data is then used to analyze the resume and optimize it to better match the provided job description, improving its chances of passing Applicant Tracking Systems (ATS).

## Features
- Generate optimize resume and cover latter
- Chat with agent to make changes on the generated resume and cover letter
- Download resume as pdf or word Document on the frontend

## Tech Stack
- Python
- FastApi
- Gemini(LLM)
- React
- Tailwind css

## API Endpoints
 - http://127.0.0.1:8000/resume/optimize/
 - http://127.0.0.1:8000/chat/agent/

## Future Improvements
- base on user requirements

## System Architectures
![Architecture Diagram](backend\resume-optimizer\flowChart\SubmitFlow.drawio.svg)


## Frontend UI