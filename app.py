from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import streamlit as st

from resume_parser import ResumeParseError, extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, load_skill_dictionary
from job_matcher import load_job_roles, rank_roles, analyze_target_role
from roadmap_generator import build_learning_roadmap

MAX_UPLOAD_MB = 5

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption("An educational tool for exploring job-related skill alignment — not an automated hiring decision.")

with st.sidebar:
    st.header("Analysis settings")
    st.info(f"Maximum upload size: {MAX_UPLOAD_MB} MB")
    st.caption("Files are processed in memory and are not saved by this application.")
    st.warning("A missing keyword does not prove that you lack a skill. Review the extracted text and results.")

uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
if not uploaded:
    st.markdown("""
    ### How it works
    1. Upload a PDF or DOCX resume.
    2. The app extracts and cleans its text.
    3. Job-related skills are identified from a controlled dictionary.
    4. TF-IDF/cosine similarity and skill coverage rank the available roles.
    5. Select a target role to see skill gaps and a learning roadmap.
    """)
    st.stop()

if uploaded.size > MAX_UPLOAD_MB * 1024 * 1024:
    st.error(f"File is too large. Please upload a file smaller than {MAX_UPLOAD_MB} MB.")
    st.stop()

try:
    raw_text = extract_resume_text(uploaded.getvalue(), uploaded.name)
except ResumeParseError as exc:
    st.error(str(exc))
    st.stop()

cleaned_text = clean_text(raw_text)
if len(cleaned_text.strip()) < 30:
    st.error("Very little text could be extracted. This may be a scanned/image-only PDF. Try a text-based PDF or DOCX.")
    st.stop()

skills_df = load_skill_dictionary()
roles_df = load_job_roles()
found_skills = extract_skills(cleaned_text, skills_df)

st.success(f"Successfully processed: {uploaded.name}")
with st.expander("Preview extracted resume text", expanded=False):
    st.text(cleaned_text[:12000])
    if len(cleaned_text) > 12000:
        st.caption("Preview truncated to 12,000 characters.")

st.subheader("Skills detected")
if found_skills:
    grouped = {}
    for item in found_skills:
        grouped.setdefault(item["category"], []).append(item["skill"])
    cols = st.columns(2)
    for index, (category, names) in enumerate(sorted(grouped.items())):
        with cols[index % 2]:
            st.markdown(f"**{category}**")
            st.write(", ".join(names))
else:
    st.warning("No dictionary skills were detected. Check the extracted text or update data/skill_dictionary.csv.")

ranked = rank_roles(cleaned_text, found_skills, roles_df)
st.subheader("Recommended job roles")
top_three = ranked.head(3).copy()
chart = px.bar(top_three.sort_values("match_score"), x="match_score", y="role",
               orientation="h", range_x=[0, 100], text="match_score",
               labels={"match_score": "Estimated match (%)", "role": "Job role"})
chart.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
st.plotly_chart(chart, use_container_width=True)
st.dataframe(ranked[["role", "match_score", "skill_coverage", "cosine_similarity"]]
             .rename(columns={"role":"Role", "match_score":"Estimated match (%)",
                               "skill_coverage":"Skill coverage (%)",
                               "cosine_similarity":"Text similarity (%)"}),
             hide_index=True, use_container_width=True)

roles = roles_df["role"].tolist()
target_role = st.selectbox("Choose a target role for detailed skill-gap analysis", roles)
analysis = analyze_target_role(target_role, found_skills, roles_df)
st.subheader(f"Skill-gap analysis: {target_role}")
left, right = st.columns(2)
with left:
    st.markdown("**Skills found in resume**")
    st.write(", ".join(analysis["found"]) if analysis["found"] else "None detected")
with right:
    st.markdown("**Required skills not detected**")
    st.write(", ".join(analysis["missing"]) if analysis["missing"] else "No missing dictionary skills detected")

st.metric("Target-role estimated match", f'{analysis["match_score"]:.1f}%')
roadmap = build_learning_roadmap(analysis["missing"])
st.subheader("Suggested learning roadmap")
if roadmap:
    for item in roadmap:
        st.markdown(f'**{item["week"]} — {item["skill"]}**')
        st.write(item["action"])
else:
    st.success("No skill gaps were detected against this role's current dataset. Consider building projects to demonstrate proficiency.")

report = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "filename": uploaded.name,
    "target_role": target_role,
    "detected_skills": found_skills,
    "ranked_roles": ranked.to_dict(orient="records"),
    "target_analysis": analysis,
    "roadmap": roadmap,
    "notice": "Educational estimate only; not a hiring decision."
}
st.download_button("⬇️ Download analysis report (JSON)",
                   data=json.dumps(report, indent=2), file_name="resume_analysis_report.json",
                   mime="application/json")
st.download_button("⬇️ Download role ranking (CSV)",
                   data=ranked.to_csv(index=False).encode("utf-8"),
                   file_name="role_recommendations.csv", mime="text/csv")

with st.expander("Method and limitations"):
    st.write("The score combines TF-IDF cosine similarity (70%) and required-skill coverage (30%). "
             "It is a transparent heuristic, not a trained hiring model. Role requirements are a small "
             "manually maintained educational dataset. Keyword matching can miss synonyms or context.")
    st.write("The system intentionally does not use gender, age, religion, nationality, photograph, "
             "marital status, disability, or other protected personal attributes.")
