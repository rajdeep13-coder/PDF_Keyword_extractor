# PDF Keyword Extractor Web

A web-based application to extract keywords and summaries from PDF documents with OCR support for scanned PDFs.

## Features
- Extract text from PDFs (supports OCR for scanned PDFs)
- Keyword extraction using Frequency or TF-IDF methods
- Automatic text summarization
- User-friendly web interface

## Installation

1. **Install dependencies:**
   - Install Tesseract OCR and Poppler:
     - **Windows**: [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki), [Poppler](http://blog.alivate.com.au/poppler-windows/)
     - **macOS**: `brew install tesseract poppler`
     - **Linux**: `sudo apt install tesseract-ocr poppler-utils`

2. **Clone the repository:**
   ```bash
   git clone https://github.com/rajdeep13-coder/PDF_Keyword_extractor.git
   cd PDF_Keyword_extractor
