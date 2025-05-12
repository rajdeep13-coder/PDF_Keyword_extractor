# PDF Keyword Extractor Web

A web-based application to extract keywords and summaries from PDF documents, with OCR support for scanned PDFs. The app uses Flask for the web interface, PyMuPDF for PDF text extraction, and Tesseract OCR for scanned PDFs. Keyword extraction is available via Frequency and TF-IDF methods, and automatic text summarization is provided.

## Features
- Extract text from PDFs (supports OCR for scanned PDFs)
- Keyword extraction using Frequency or TF-IDF methods
- Automatic text summarization
- Custom stopwords support (via `data/stopwords.txt`)
- User-friendly web interface

## Installation

### 1. Install System Dependencies
- **Tesseract OCR** and **Poppler** are required for OCR and PDF-to-image conversion.
  - **Windows:**
    - [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    - [Poppler](http://blog.alivate.com.au/poppler-windows/)
    - Ensure Tesseract is installed in `C:\Program Files\Tesseract-OCR\tesseract.exe` or `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`, or update the path in your system environment variables.
  - **macOS:**
    - `brew install tesseract poppler`
  - **Linux:**
    - `sudo apt install tesseract-ocr poppler-utils`

### 2. Clone the Repository
```bash
git clone https://github.com/rajdeep13-coder/PDF_Keyword_extractor.git
cd PDF_Keyword_extractor
```

### 3. Install Python Dependencies
It is recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. **Start the Application:**
   ```bash
   python app.py
   ```
   The app will run on `http://127.0.0.1:5000/` by default.

2. **Upload a PDF:**
   - Go to the web interface.
   - Upload a PDF file.
   - Choose the keyword extraction method (Frequency or TF-IDF).
   - The app will display extracted keywords and a summary.

3. **OCR Support:**
   - If the PDF is scanned or contains images, OCR will be automatically used if text extraction fails or is insufficient.
   - Ensure Tesseract and Poppler are installed and accessible.

## Project Structure
```
PDF_Keyword_extractor/
├── app.py                  # Main Flask application
├── extractor/
│   ├── keyword_finder.py   # Keyword extraction and summarization logic
│   └── pdf_reader.py       # PDF text extraction with OCR support
├── data/
│   └── stopwords.txt       # Custom stopwords (optional)
├── static/
│   └── styles.css          # CSS styles
├── templates/
│   └── index.html          # Web interface template
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Configuration
- **Secret Key:** The Flask app uses a secret key from the `SECRET_KEY` environment variable, or defaults to `'your_secret_key_here'`.
- **Stopwords:** You can customize stopwords by editing `data/stopwords.txt`.

## Dependencies
- Flask
- nltk
- scikit-learn
- gensim
- scipy
- PyMuPDF
- Pillow
- gunicorn (for production deployment)
- pdf2image
- pytesseract

## Notes
- For best OCR results, ensure Tesseract and Poppler are correctly installed and configured in your system PATH.
- The app will automatically use OCR if the extracted text is too short or if explicitly requested in the code.
- Summarization uses a TF-IDF-based approach for sentence ranking.

## License
MIT License
