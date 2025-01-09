import pytesseract
from pdf2image import convert_from_path
from ollama import ChatResponse, chat

# Set the Tesseract executable path if it's not in your PATH environment variable
pytesseract.pytesseract.tesseract_cmd = r"E:\MyOCR\teseractOCR\tesseract.exe"

def extract_text_from_pdf(pdf_path, language='eng'):
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for i, image in enumerate(images):
        page_text = pytesseract.image_to_string(image, lang=language)
        extracted_text += f"--- Page {i + 1} ---\n{page_text}\n"

    return extracted_text

def image_pdf_process(pdf_path, user_input):
    # pdf_path = r"C:\Users\dheer\Downloads\dheeraj__warkar__res.pdf"  # Replace with your PDF path
    language = 'eng'  # Specify the OCR language
    extracted_text = extract_text_from_pdf(pdf_path, language)
    print("Extracted Text:\n")
    print(extracted_text)

    # Define user query
    # user_input = "What is the exact work experience tenure?"

    # Pass the extracted text and user input to the chat function
    response: ChatResponse = chat(
        model='llama3.2',
        messages=[
            {
                'role': 'user',
                'content': extracted_text + "\n\n" + user_input,
            },
        ],
    )

    # Print the AI's response

    return(response['message']['content'])
