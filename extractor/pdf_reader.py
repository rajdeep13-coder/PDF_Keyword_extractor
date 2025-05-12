import os
import re
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader
import fitz  

class PDFTextExtractor:
    def __init__(self):
        self.text = ""
        
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 
        self.poppler_path = r"C:\poppler\bin"  
        
    def extract_text(self, pdf_path, use_ocr=False):
        try:
            if use_ocr:
                self._extract_with_ocr(pdf_path)
            else:
                reader = PdfReader(pdf_path)
                self.text = " ".join([page.extract_text() or "" for page in reader.pages])
          
            if len(self.text.strip()) < 100:
                self._extract_with_ocr(pdf_path)
            return self.clean_raw_text()
        except Exception as e:
            raise RuntimeError(f"PDF read error: {str(e)}")

    def _extract_with_ocr(self, pdf_path):
        try:
           
            images = convert_from_path(pdf_path, poppler_path=self.poppler_path)
            self.text = "\n".join([pytesseract.image_to_string(img) for img in images])
        except Exception as e:
            raise RuntimeError(
                f"OCR failed: {str(e)}. Make sure Tesseract-OCR and Poppler are installed and correctly configured."
            )

    def clean_raw_text(self):
        """Clean and normalize the extracted text."""
        return re.sub(r'\s+', ' ', self.text).strip()
