import re
def simple_tokenize(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub(r'[\r\n\t]', ' ', text)
    text = re.sub(r'[^a-z0-9+# ]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 1]
    return tokens
def extract_skills_from_text(text, skills_vocab=None):
    tokens = simple_tokenize(text)
    if skills_vocab:
        found = set()
        for skill in skills_vocab:
            key = skill.lower()
            if key in text.lower():
                found.add(skill)
        return sorted(list(found))
    else:
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [it[0] for it in items[:20]]
