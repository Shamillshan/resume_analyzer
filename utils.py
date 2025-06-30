import re
import spacy

# Load spaCy medium model with word vectors
nlp = spacy.load("en_core_web_md")

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-\(\)]{9,}\d', text)
    return match.group(0) if match else "Not found"

def extract_skills(text, skill_list, similarity_threshold=0.75):
    doc = nlp(text)
    found_skills = set()

    # NER-based matching
    for ent in doc.ents:
        for skill in skill_list:
            if skill.lower() in ent.text.lower():
                found_skills.add(skill)

    # Semantic similarity matching
    for skill in skill_list:
        skill_doc = nlp(skill)
        for token in doc:
            if token.has_vector and skill_doc.has_vector:
                if token.similarity(skill_doc) >= similarity_threshold:
                    found_skills.add(skill)
                    break

    return list(found_skills)
