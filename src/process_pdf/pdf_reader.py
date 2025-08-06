import fitz
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    
    return text

def pdf_preprocess(pdf_file) -> str:
    """
    Extracts text from an uploaded PDF file.

    Args:
        pdf_file: The uploaded PDF file object.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        # Open the PDF from the file-like object
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf_document:
            for page in pdf_document:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    
    return text
