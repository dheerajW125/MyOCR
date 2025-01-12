import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
import uvicorn
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from text_based_ext.txt_extraction import txt_pdf_process
from image_based_ext.img_extract import image_pdf_process
import fitz

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_text_pdf(file_path: str) -> bool:
    try:
        pdf_document = fitz.open(file_path)

        for page in pdf_document:
            if page.get_text(): 
                return True
        return False
    except Exception as e:
        raise ValueError(f"Error while checking PDF type: {str(e)}")

@app.post('/process_pdfs')
async def process_pdf(file: UploadFile, prompt: Optional[str] = Form(...)):
    try:
        if not file:
            return JSONResponse({"error": "No file part"}, status_code=400)

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_content = await file.read() 
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        if is_text_pdf(tmp_file_path): 
            extracted_txt = txt_pdf_process(tmp_file_path, prompt)
        else:
            extracted_txt = image_pdf_process(tmp_file_path, prompt)

        os.remove(tmp_file_path)

        return JSONResponse(content={"msg": extracted_txt}, status_code=200)
    
    except Exception as e:

        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
