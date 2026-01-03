# D:\ATS_project\app.py

import streamlit as st
import json

# Import functions from our src folder
from src.pdf_parser import extract_text_from_pdf
from src.text_processor import preprocess_text
from src.info_extractor import extract_entities # This function now needs 'spacy_model' passed to it
from src.matcher import get_matching_score
from src.utils import load_spacy_model, load_sentence_transformer_model

# --- THIS MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(page_title="Resume to Job Description Matcher", layout="wide")
# --- END OF SET_PAGE_CONFIG ---

# Initialize models (Streamlit's st.cache_resource handles single loading)
spacy_model = None
sentence_transformer_model = None

# Use try-except blocks to catch model loading errors AFTER set_page_config()
try:
    with st.spinner("Loading SpaCy model..."):
        spacy_model = load_spacy_model()
except RuntimeError as e:
    st.error(f"**Critical Error:** {e}")
    st.info("The app cannot function without the SpaCy model. Please check your internet connection or model installation.")
    st.stop() # Stop the app if a critical model can't be loaded

try:
    with st.spinner("Loading Sentence Transformer model..."):
        sentence_transformer_model = load_sentence_transformer_model()
except RuntimeError as e:
    st.error(f"**Critical Error:** {e}")
    st.info("The app cannot function without the Sentence Transformer model. Please check your internet connection or model installation.")
    st.stop() # Stop the app if a critical model can't be loaded

st.title("🤝 Resume to Job Description Matcher")
st.markdown("Upload your resume (PDF) and paste a job description to find out how well you match!")

# Layout: two columns for input, one for output
col1, col2 = st.columns(2)

resume_raw_text = ""
job_description_raw_text = ""

with col1:
    st.subheader("Your Resume (PDF)")
    uploaded_resume = st.file_uploader("Upload PDF File", type=["pdf"], key="resume_uploader")
    if uploaded_resume:
        st.info("Extracting text from resume...")
        resume_raw_text = extract_text_from_pdf(uploaded_resume)
        if not resume_raw_text:
            st.error("Could not extract text from resume. Please try a different PDF or ensure it's not scanned/image-based.")
        else:
            st.success("Resume text extracted!")
            with st.expander("View Extracted Resume Text"):
                st.text(resume_raw_text[:2000] + "..." if len(resume_raw_text) > 2000 else resume_raw_text)

with col2:
    st.subheader("Job Description (Text)")
    job_description_raw_text = st.text_area("Paste Job Description here:", height=400, key="job_desc_input")
    if job_description_raw_text:
        if not job_description_raw_text.strip():
            st.warning("Job description is empty.")
        else:
            st.success("Job description ready.")
            with st.expander("View Job Description Text"):
                st.text(job_description_raw_text[:2000] + "..." if len(job_description_raw_text) > 2000 else job_description_raw_text)

st.markdown("---")

if st.button("✨ Get Match Score", type="primary"):
    if not resume_raw_text:
        st.error("Please upload a resume first.")
    elif not job_description_raw_text.strip():
        st.error("Please paste a job description first.")
    else:
        with st.spinner("Calculating match score... This may take a moment."):
            # 1. Preprocess texts
            preprocessed_resume = preprocess_text(resume_raw_text)
            preprocessed_job_description = preprocess_text(job_description_raw_text)

            # 2. Extract entities (skills, qualifications, etc.)
            st.text("Extracting key information...")
            # IMPORTANT: Pass the loaded spacy_model here
            resume_entities = extract_entities(resume_raw_text, spacy_model) # Pass spacy_model
            job_entities = extract_entities(job_description_raw_text, spacy_model) # Pass spacy_model

            # 3. Calculate matching score
            st.text("Calculating similarity...")
            match_result = get_matching_score(
                preprocessed_resume, preprocessed_job_description,
                resume_entities, job_entities
            )

            st.markdown("---")
            st.success("🎉 Match Score Calculated!")

            st.metric(label="Overall Match Score", value=f"{match_result['overall_score']}%")

            st.subheader("Match Score Breakdown:")
            for aspect, score in match_result['breakdown'].items():
                st.write(f"- **{aspect.replace('_', ' ').title()}:** {round(score * 100, 2)}%")

            st.subheader("Extracted Information:")
            col_res_ent, col_job_ent = st.columns(2)
            with col_res_ent:
                st.markdown("#### From Resume")
                st.json(resume_entities)
            with col_job_ent:
                st.markdown("#### From Job Description")
                st.json(job_entities)

            st.markdown("---")
            st.info("Remember: This is a simplified model. For production, you'd need more sophisticated NER, experience parsing, and a fine-tuned scoring algorithm with real-world data.")