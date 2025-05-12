from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import fitz  
from extractor.keyword_finder import KeywordProcessor
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded')
            return render_template('index.html')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                method = request.form.get('method', 'frequency')
                text = extract_text_from_pdf(filepath)
                processor = KeywordProcessor()
                keywords = processor.get_keywords(text, method=method)
                summary = processor.summarize_text(text)
                os.remove(filepath)
                return render_template('index.html', 
                                       keywords=keywords,
                                       summary=summary,
                                       filename=filename)
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Error processing file: {str(e)}')
                return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)