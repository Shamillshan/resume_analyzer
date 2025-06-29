import streamlit as st
from resume_parser import extract_text
from utils import extract_email, extract_phone, extract_skills
import json

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("Resume Analyzer App")

# Load job roles and skills
with open("job_roles.json", "r") as f:
    job_data = json.load(f)

uploaded_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", text, height=250)

    st.subheader("🔍 Extracted Information")
    email = extract_email(text)
    phone = extract_phone(text)
    st.markdown(f"- **Email**: {email}")
    st.markdown(f"- **Phone**: {phone}")

    selected_role = st.selectbox("Select Job Role", list(job_data.keys()))
    required_skills = job_data[selected_role]
    found_skills = extract_skills(text, required_skills)

    score = len(found_skills) / len(required_skills) * 100
    st.metric(label="🎯 Skill Match Score", value=f"{score:.1f}%")

    st.success(f"✅ Found Skills: {', '.join(found_skills)}")
    missing = list(set(required_skills) - set(found_skills))
    st.error(f"❌ Missing Skills: {', '.join(missing)}")
