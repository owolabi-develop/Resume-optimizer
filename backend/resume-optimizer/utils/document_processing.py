import pymupdf
from docx import Document
from io import BytesIO

class ProcessDocument:
    def __init__(self,file):
        self.file = file

    def process_pdf_file(self):
        doc = pymupdf.open(stream=self.file,filetype="pdf")
        fullText = ""
        for page in doc:
            text = page.get_text()
            fullText += text
        return fullText.split("\n")
        




    def process_docx_file(self):
         source_stream = BytesIO(self.file)
         doc = Document(source_stream)
        
         fullText = []

         for para in doc.paragraphs:
            print(para)
            fullText.append(para.text)
         return '\n'.join(fullText) 

         