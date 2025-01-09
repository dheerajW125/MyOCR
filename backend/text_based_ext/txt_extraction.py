import fitz
import re
import ollama
from ollama import chat
from ollama import ChatResponse
import fitz

def label_text_file(pdf_path):
        pdf_document = fitz.open(pdf_path)
        list_of_text = []
 
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text = page.get_text()
            list_of_text.append(text)
 
        pdf_document.close()
 
        block_text = '\n'.join(list_of_text)
        # print(block_text)
        return block_text
           

def txt_pdf_process(pdf_path, user_input):
# user_input ="What is the exact work experience tenure"
    text = label_text_file(pdf_path)
    response: ChatResponse = chat(
        model='llama3.2',
        messages=[
            {
                'role': 'user',
                'content': text + user_input,
            },
        ],
    )
    

    return(response['message']['content'])