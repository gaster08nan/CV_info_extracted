from PIL import Image
from pathlib import Path
# from paddleocr import PaddleOCR
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import fitz


def save_pdf_to_image(pdf_path):
    """
    Converts each page of a PDF to an image and saves it.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where images will be saved.
    """
    try:
        pdf_document = fitz.open(pdf_path)
        img_lst = []
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_lst.append(img)
        
        return img_lst
                
    except Exception as e:
        print(f"Error converting PDF to images: {e}")

def define_model():
    model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
    return model

def ocr_image(pdf_path: str, model):
    pdf_doc = DocumentFile.from_pdf(Path(pdf_path))
    result = model(pdf_doc)
    text = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    # print(word.value)
                    # breakpoint()
                    text += [word.value]
            text += ["\n"]
    text = [t.strip() for t in text if t.strip()]
    return " ".join(text)

if __name__ == "__main__": 
    pdf_path = '../../datasets/data/INFORMATION-TECHNOLOGY/10089434.pdf'
    model = define_model()
    page_content = ocr_image(pdf_path, model)
    print(page_content)
    # img_lst = save_pdf_to_image(pdf_path)
    # page_content = ocr_image(img_lst)
    # print("\n".join(page_content))
