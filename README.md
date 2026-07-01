# AI-Powered Resume Screener (Polished)

This is a polished, ready-to-run AI Resume Screener for your college PBL and interview portfolio.
It extracts text from resumes (TXT, DOCX, PDF), computes similarity to a job description using TF-IDF + cosine similarity (normalized to 0-100%), ranks resumes, and provides a Streamlit UI with downloadable results.

## Features
- Robust resume parsing (txt, docx, pdf)
- No NLTK dependency (uses regex + sklearn)
- Normalized similarity scores (0-100%)
- Streamlit UI with file upload, preview, rank table, chart, and CSV download
- Sample resumes and job description included
- Auto-generated simple PPTX and Word report (if python-pptx and python-docx are installed)

## Quick Start
1. Create & activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (cmd):
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app from the project root (important):
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Notes
- Run the app from the project root so imports resolve correctly.
- If PDF text extraction fails for some PDFs, try converting to DOCX or TXT as fallback.
