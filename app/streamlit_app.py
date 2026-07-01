import streamlit as st
import sys, os
from pathlib import Path
import pandas as pd
import base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parser import extract_text
from src.screener import score_resumes
st.set_page_config(page_title='AI Resume Screener', layout='wide')
st.title('AI-Powered Resume Screener')
st.sidebar.header('Upload & Job Description')
uploaded_files = st.sidebar.file_uploader('Upload resumes (txt, docx, pdf)', accept_multiple_files=True)
job_text = st.sidebar.text_area('Paste job description here', height=200)
if st.sidebar.button('Use sample job description'):
    job_text = Path('data/job_description.txt').read_text()
    st.sidebar.success('Loaded sample job description')
if uploaded_files and job_text.strip():
    st.info('Processing resumes...')
    texts = []
    names = []
    for f in uploaded_files:
        out_path = Path('data/resumes') / f.name
        with open(out_path, 'wb') as out:
            out.write(f.getbuffer())
        txt = extract_text(out_path)
        texts.append(txt)
        names.append(f.name)

    results = score_resumes(texts, job_text)

    df_rows = []
    for r in results:
        idx = r['resume_idx']
        df_rows.append({'File': names[idx], 'Score': r['score'], 'Matched': ', '.join(r['matched_skills'])})

    df = pd.DataFrame(df_rows)
    if df.empty:
        st.warning('No valid resumes processed.')
    else:
        df = df.sort_values('Score', ascending=False).reset_index(drop=True)
        df['Rank'] = df.index + 1
        st.success('Ranking complete')
        st.dataframe(df[['Rank','File','Score']])

        st.subheader('Scores')
        chart_df = df[['File','Score']].set_index('File')
        st.bar_chart(chart_df)

        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="ranked_resumes.csv">Download ranked results (CSV)</a>'
        st.markdown(href, unsafe_allow_html=True)

        top = results[0]
        st.markdown(f"### 1. {names[top['resume_idx']]} — {top['score']}%")
        st.markdown('**Matched (heuristic):** ' + (', '.join(top['matched_skills']) or 'None'))
        st.text_area('Extracted text (preview)', texts[top['resume_idx']][:1000], height=300)
else:
    st.info('Upload resumes and paste a job description to run the screener.')
    st.write('You can also click "Use sample job description" in the sidebar.')