\
@echo off
if exist .venv\Scripts\Activate.bat (
    call .venv\Scripts\Activate.bat
)
python -m streamlit run app/streamlit_app.py
