import streamlit as st
from resume_parser import extract_text
from utils import extract_email, extract_phone, extract_skills
import json

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.markdown("<h1 style='text-align: center;'>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

with open("job_roles.json", "r") as f:
    job_data = json.load(f)

col1, col2 = st.columns([2, 2])
with col1:
    uploaded_file = st.file_uploader("📤 Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
with col2:
    selected_role = st.selectbox("💼 Select Job Role", list(job_data.keys()))


if uploaded_file:
    text = extract_text(uploaded_file)

    st.markdown("### 🧾 Extracted Resume Text")
    st.text_area("Resume Content", text, height=200)

    st.markdown("### 🔍 Extracted Information")
    col_email, col_phone = st.columns(2)
    with col_email:
        st.metric("📧 Email", extract_email(text))
    with col_phone:
        st.metric("📞 Phone", extract_phone(text))

    # Skill Analysis
    required_skills = job_data[selected_role]
    found_skills = extract_skills(text, required_skills)
    missing_skills = list(set(required_skills) - set(found_skills))
    score = len(found_skills) / len(required_skills) * 100

    st.markdown("### 🎯 Skill Match Summary")
    st.metric("Skill Match Score", f"{score:.1f}%")

    col_match, col_missing = st.columns(2)
    with col_match:
        st.success("✅ Found Skills")
        st.markdown(", ".join(found_skills) if found_skills else "_None_")
    with col_missing:
        st.error("❌ Missing Skills")
        st.markdown(", ".join(missing_skills) if missing_skills else "_None_")
