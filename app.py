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
submit3 = st.button("Good/Bad match")

input_prompt1 = """
You are a resume parser. You will be given a job description and a resume.
Your task is to extract the relevant information from the resume and provide a summary of the
candidate's qualifications and experience in relation to the job description.
"""

input_prompt2 = """
You are a skilled ATS(Applicant Tracking System) parser. You will be given a job description and 
a resume. Your job is to find the percentage match between the two.
"""
input_prompt3 = """
You are a very experienced HR at a big software development company. You will be given a job 
description and a resume. Your job is to tell whether the candidate is a "good match" or a 
"bad match" for the role.
Consider the percentage match for this filtering as a feature as well.
For example, let's say the following is the job description for a role:
At [Company X], we rely on insightful data to power our systems and solutions. We’re seeking an 
experienced data scientist to deliver insights on a daily basis. The ideal candidate will have 
mathematical and statistical expertise, along with natural curiosity and a creative mind. While 
mining, interpreting, and cleaning our data, this person will be relied on to ask questions, connect
 the dots, and uncover hidden opportunities for realizing the data’s full potential. As part of a 
team of specialists, the data scientist will “slice and dice” data using various methods and create 
new visions for the future.

Objectives of this role:
Collaborate with product design and engineering teams to develop an understanding of needs
Research and devise innovative statistical models for data analysis
Communicate findings to all stakeholders
Enable smarter business processes by using analytics for meaningful insights
Keep current with technical and industry developments

Responsibilities:
Serve as lead data strategist to identify and integrate new datasets that can be leveraged through
 our product capabilities, and work closely with the engineering team in the development of data 
products
Execute analytical experiments to help solve problems across various domains and industries
Identify relevant data sources and sets to mine for client business needs, and collect large structured 
and unstructured datasets and variables
Devise and utilize algorithms and models to mine big-data stores; perform data and error analysis to 
improve models; clean and validate data for uniformity and accuracy
Analyze data for trends and patterns, and interpret data with clear objectives in mind
Implement analytical models in production by collaborating with software developers and machine-learning
engineers

Required skills and qualifications:
Seven or more years of experience in data science
Proficiency with data mining, mathematics, and statistical analysis
Advanced experience in pattern recognition and predictive modeling
Experience with Excel, PowerPoint, Tableau, SQL, and programming languages (ex: Java/Python, SAS)
Ability to work effectively in a dynamic, research-oriented group that has several concurrent projects
Preferred skills and qualifications
Bachelor’s degree (or equivalent) in statistics, applied mathematics, or related discipline
Two or more years of project management experience
Professional certification

If the following resume is provided:
Name: ABC
College: XYZ
Experience: 12 years being a data analyst at abc, apt in data mining, EDA, Python, Deep Learning, Excel etc.
Projects: Many projects in NLP, CV, Data Science, AI etc

Then this resume is a good match

if another resume is provided as:
Name: ABC
College: XYZ
Experience: No prior experience, data science, Game development, product management etc.
Projects: only very basic projects

Then this resume is a bad match
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
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:  # Check if pdf_content is not None
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The response is: ")
            st.write(response)
        else:
            st.error("Could not extract text from PDF.")
    else:
        st.error("Please upload a PDF file.")
