
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

my_api_key = "YOUR_GEMINI_API_KEY"


# Load environment variables
#load_dotenv()

# Configure Google AI
#my_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=my_api_key)

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech fields, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide the best assistance for improving the resumes. Assign the percentage Matching based on JD and the missing keywords with high accuracy

resume: {text}
description: {jd}

I want the response in one single string having the structure {{"JD Match":"%","MissingKeywords:[]","Profile Summary":"", "Improvement Suggestions":[]}}
"""

# Streamlit app
st.set_page_config(page_title="Smart ATS", page_icon="📄", layout="wide")

st.title("🚀 Smart ATS - Resume Analyzer")
st.markdown("### Improve Your Resume and Match Job Descriptions")

col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("Paste the Job Description", height=300)

with col2:
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload a PDF file")

submit = st.button("Analyze Resume")

if submit:
    if uploaded_file is not None and jd:
        with st.spinner("Analyzing your resume..."):
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))
            
            try:
                response_dict = json.loads(response)
                
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("JD Match", response_dict["JD Match"])
                
                with col2:
                    st.subheader("Missing Keywords")
                    st.write(", ".join(response_dict["MissingKeywords"]))
                
                st.subheader("Profile Summary")
                st.info(response_dict["Profile Summary"])
                
                st.subheader("Improvement Suggestions")
                for idx, suggestion in enumerate(response_dict["Improvement Suggestions"], 1):
                    st.write(f"{idx}. {suggestion}")
                
            except json.JSONDecodeError:
                st.error("Error parsing the response. Please try again.")
    else:
        st.warning("Please upload a PDF resume and provide a job description.")

st.markdown("---")
st.markdown("### How to use this tool:")
st.markdown("""
1. Paste the job description in the left text area.
2. Upload your resume in PDF format.
3. Click the 'Analyze Resume' button.
4. Review the analysis results and suggestions to improve your resume.
""")

st.sidebar.title("About")
st.sidebar.info(
    "This app uses AI to analyze your resume against a job description. "
    "It provides insights on how well your resume matches the job requirements "
    "and offers suggestions for improvement."
)
st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️ by [SHIVAN KUMAR]")