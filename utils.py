import re

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-\(\)]{9,}\d', text)
    return match.group(0) if match else "Not found"

def extract_skills(text, skill_list):
    text = text.lower()
    return [skill for skill in skill_list if skill.lower() in text]
