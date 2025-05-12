import os
import re
import platform
import shutil
from pdf2image import convert_from_path
import pytesseract
import fitz  

class PDFTextExtractor:
    def __init__(self):
        self.text = ""
        
        # Set up Tesseract path based on operating system
        self._setup_tesseract_path()
        
    def _setup_tesseract_path(self):
        """Set up the correct Tesseract path based on OS."""
        system = platform.system()
        
        if system == "Windows":
            # Check common installation locations
            possible_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
        elif system == "Linux":
            # On Linux, check if tesseract is available in PATH
            if shutil.which("tesseract"):
                pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")
        # On macOS, pytesseract typically finds tesseract automatically if installed
        
    def extract_text(self, pdf_path, use_ocr=False):
        try:
            # Use PyMuPDF as the primary method
            if not use_ocr:
                with fitz.open(pdf_path) as doc:
                    self.text = " ".join([page.get_text() for page in doc])
          
            # If extracted text is too short or OCR is requested, try OCR
            if len(self.text.strip()) < 100 or use_ocr:
                self._extract_with_ocr(pdf_path)
                
            return self.clean_raw_text()
        except Exception as e:
            raise RuntimeError(f"PDF read error: {str(e)}")

    def _extract_with_ocr(self, pdf_path):
        try:
            # Convert PDF to images (pdf2image finds poppler automatically if in PATH)
            images = convert_from_path(pdf_path)
                
            # Extract text from images
            self.text = "\n".join([pytesseract.image_to_string(img) for img in images])
        except Exception as e:
            raise RuntimeError(
                f"OCR failed: {str(e)}. Make sure Tesseract-OCR is installed and correctly configured."
            )

    def clean_raw_text(self):
        """Clean and normalize the extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', self.text).strip()
        # Remove common PDF artifacts
        text = re.sub(r'(\n\s*)+', '\n', text)
        return text