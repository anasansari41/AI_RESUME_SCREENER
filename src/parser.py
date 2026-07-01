from pathlib import Path
import PyPDF2
import docx

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text_from_docx(path):
    doc = docx.Document(path)
    texts = [p.text for p in doc.paragraphs]
    return '\n'.join(texts)

def extract_text_from_pdf(path):
    texts = []
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            try:
                texts.append(page.extract_text() or '')
            except Exception:
                texts.append('')
    return '\n'.join(texts)

def extract_text(path):
    p = Path(path)
    if not p.exists():
        return ''
    suf = p.suffix.lower()
    try:
        if suf == '.txt':
            return extract_text_from_txt(p)
        elif suf == '.docx':
            return extract_text_from_docx(p)
        elif suf == '.pdf':
            return extract_text_from_pdf(p)
        else:
            return ''
    except Exception as e:
        return ''
