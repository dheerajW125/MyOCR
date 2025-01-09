from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Optional
from text_based_ext.txt_extraction import txt_pdf_process
from image_based_ext.img_extract import image_pdf_process
import fitz


app = FastAPI


def is_text_pdf(file_path: str) -> bool:
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                if page.get_text(): 
                    return True
        return False
    except Exception as e:
        raise ValueError(f"Error while checking PDF type: {str(e)}")

@app.post('/process_pdfs')
async def process_pdf(file: UploadFile, prompt:Optional[str]= Form(...)):
    try:
        if not file:
            return JSONResponse({"error": "No file part"}, status_code= 400)
        if is_text_pdf(file):
            extracted_txt =txt_pdf_process(file)
        else:
            extracted_txt = image_pdf_process(file)
        return JSONResponse(content={"msg": extracted_txt}, status_code=200)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


