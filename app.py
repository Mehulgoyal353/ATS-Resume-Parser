import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import base64
import io
import google.generativeai as genai
from PyPDF2 import PdfReader  # Import PyPDF2

# --- Load API Key and Configure Gemini ---
api_key = st.secrets["GOOGLE_API_KEY"]
if not api_key:
    st.error("No GOOGLE_API_KEY found in Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content, prompt])  # Modified
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text  # Return the extracted text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="ATS Resume Parser")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description", key = "input")
uploaded_file = st.file_uploader("Upload your Resume(PDF format)")

if uploaded_file is not None:
    st.write("PDF file uploaded successfully.")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("Percentage match")

input_prompt1 = """
You are a resume parser. You will be given a job description and a resume.
Your task is to extract the relevant information from the resume and provide a summary of the
candidate's qualifications and experience in relation to the job description.
"""

input_prompt2 = """
You are a skilled ATS(Applicant Tracking System) parser. You will be given a job description and 
a resume. Your job is to find the percentage match between the two.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:  # Check if pdf_content is not None
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The response is: ")
            st.write(response)
        else:
            st.error("Could not extract text from PDF.")
    else:
        st.error("Please upload a PDF file.")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:  # Check if pdf_content is not None
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("The response is: ")
            st.write(response)
        else:
            st.error("Could not extract text from PDF.")
    else:
        st.error("Please upload a PDF file.")
