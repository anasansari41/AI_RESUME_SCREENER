from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
model = SentenceTransformer('all-MiniLM-L6-v2')
SKILLS = [
    "python", "machine learning", "deep learning", "nlp",
    "data analysis", "data science", "sql", "pandas",
    "numpy", "tensorflow", "pytorch", "excel",
    "tableau", "power bi", "statistics"
]
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text
def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]
def score_resumes(resumes, job_text):
    job_text = clean_text(job_text)
    resumes_clean = [clean_text(r) for r in resumes]

    job_emb = model.encode([job_text])
    res_emb = model.encode(resumes_clean)

    sim_scores = cosine_similarity(job_emb, res_emb)[0]

    results = []

    job_skills = set(extract_skills(job_text))

    for i, resume in enumerate(resumes_clean):
        resume_skills = set(extract_skills(resume))

        if job_skills:
            skill_match = len(job_skills & resume_skills) / len(job_skills)
        else:
            skill_match = 0

        final_score = (0.8 * sim_scores[i]) + (0.2 * skill_match)

        results.append({
            "resume_idx": i,
            "score": round(final_score * 100, 2),
            "matched_skills": list(job_skills & resume_skills)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)