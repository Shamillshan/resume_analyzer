import streamlit as st
import json
import pandas as pd
import altair as alt
import io
from fpdf import FPDF

from resume_parser import extract_text
from utils import extract_email, extract_phone, extract_skills

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.markdown("<h1 style='text-align: center;'>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

# Load job roles and skills
with open("job_roles.json", "r") as f:
    job_data = json.load(f)

# Upload section
col1, col2 = st.columns([2, 2])
with col1:
    uploaded_file = st.file_uploader("📤 Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
with col2:
    selected_role = st.selectbox("💼 Select Job Role", list(job_data.keys()))

# Resume analysis section
if uploaded_file:
    text = extract_text(uploaded_file)

    st.markdown("### 🧾 Extracted Resume Text")
    st.text_area("Resume Content", text, height=200)

    st.markdown("### 🔍 Extracted Information")
    col_email, col_phone = st.columns(2)
    with col_email:
        email = extract_email(text)
        st.metric("📧 Email", email)
    with col_phone:
        phone = extract_phone(text)
        st.metric("📞 Phone", phone)

    required_skills = job_data[selected_role]
    found_skills = extract_skills(text, required_skills)
    missing_skills = list(set(required_skills) - set(found_skills))
    score = len(found_skills) / len(required_skills) * 100

    st.markdown("### 🎯 Skill Match Summary")
    st.metric("Skill Match Score", f"{score:.1f}%")

    # Skills display
    col_match, col_missing = st.columns(2)
    with col_match:
        st.success("✅ Found Skills")
        st.markdown(", ".join(found_skills) if found_skills else "_None_")
    with col_missing:
        st.error("❌ Missing Skills")
        st.markdown(", ".join(missing_skills) if missing_skills else "_None_")

    # --- Charts section ---
    st.markdown("### 📊 Skill Match Visualization")

    skill_data = pd.DataFrame({
        "Skill Type": ["Matched Skills", "Missing Skills"],
        "Count": [len(found_skills), len(missing_skills)]
    })

    pie_chart = alt.Chart(skill_data).mark_arc(innerRadius=40).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Skill Type", type="nominal"),
        tooltip=["Skill Type", "Count"]
    ).properties(
        title=alt.TitleParams(
            text="Matched vs. Missing Skills",
            fontSize=20,
            fontWeight="bold"
        )
    ).configure_legend(
        labelFontSize=14,
        titleFontSize=16
    ).configure_view(
        strokeWidth=0
    )

    chart_col, label_col = st.columns([2, 1])
    with chart_col:
        st.altair_chart(pie_chart, use_container_width=True)

    # --- PDF Export (no emojis to avoid UnicodeEncodeError) ---
    st.markdown("### 📥 Download PDF Report")

    class PDFReport(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Resume Analysis Report", ln=True, align="C")
            self.ln(10)

        def section_title(self, title):
            self.set_font("Arial", "B", 12)
            self.set_text_color(40, 40, 40)
            self.cell(0, 10, title, ln=True)
            self.ln(1)

        def section_body(self, body):
            self.set_font("Arial", "", 11)
            self.set_text_color(20, 20, 20)
            self.multi_cell(0, 8, body)
            self.ln()

    pdf = PDFReport()
    pdf.add_page()
    pdf.section_title("Email")
    pdf.section_body(email)
    pdf.section_title("Phone")
    pdf.section_body(phone)
    pdf.section_title("Selected Job Role")
    pdf.section_body(selected_role)
    pdf.section_title("Skill Match Score")
    pdf.section_body(f"{score:.1f}%")
    pdf.section_title("Matched Skills")
    pdf.section_body(", ".join(found_skills) if found_skills else "None")
    pdf.section_title("Missing Skills")
    pdf.section_body(", ".join(missing_skills) if missing_skills else "None")

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf.output(dest="S").encode("latin-1"),
        file_name="resume_analysis.pdf",
        mime="application/pdf"
    )
