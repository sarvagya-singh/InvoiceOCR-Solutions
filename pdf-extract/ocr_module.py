import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile

def extract_text_from_pdf(file):
    # Save the uploaded file to a temporary location
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    temp_file.close()

    # Read the PDF file
    doc = fitz.open(temp_file.name)
    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_path = f"{temp_file.name}_page_{page_num}.png"
        pix.save(img_path)

        # Perform OCR on the image using pytesseract
        text = pytesseract.image_to_string(Image.open(img_path), lang='eng')
        extracted_text += text + "\n"

        # Clean up the image file
        os.remove(img_path)

    # Close and remove the temporary file
    doc.close()
    os.unlink(temp_file.name)

    return extracted_text



'''
import os
from paddleocr import PaddleOCR
import fitz
from tempfile import NamedTemporaryFile

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_pdf(file):
    # Save the uploaded file to a temporary location
    temp_file = NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    temp_file.close()

    # Read the PDF file
    doc = fitz.open(temp_file.name)
    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_path = f"{temp_file.name}_page_{page_num}.png"
        pix.save(img_path)

        # Perform OCR on the image
        result = ocr.ocr(img_path, cls=True)
        for line in result:
            for word in line:
                extracted_text += word[1][0] + " "

        # Clean up the image file
        os.remove(img_path)

    # Close and remove the temporary file
    doc.close()
    os.unlink(temp_file.name)

    return extracted_text
'''