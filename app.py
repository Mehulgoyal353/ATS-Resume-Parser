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
You are a resume parser. You will be given a job description and a resume. Your task is to 
extract the relevant information from the resume and provide a concise summary (approximately 150-200 words) 
of the candidate's key skills and relevant experience in relation to the job description. The summary 
should explicitly state how the candidate's skills and experience align with the requirements of the 
job description. Write the summary such that you are providing the summary to a hiring manager seeking 
to find a suitable candidate.

Here's an example of the kind of summary I'm looking for:

Job Description: "Seeking a Senior Software Engineer with 5+ years of experience in Java, Spring, and
 REST APIs. Strong problem-solving skills and a Bachelor's degree in Computer Science are required."

Resume: [Assume a resume with relevant Java, Spring, REST API experience and Computer Science degree]

Summary: "To the Hiring Manager: This candidate is a strong fit for the Senior Software Engineer position.
Jane Doe has 5+ years of Java and Spring development experience, directly aligning with the job description's 
requirements. She has proven experience developing REST APIs as requested.  Jane also possesses a Bachelor's 
degree in Computer Science, fulfilling the education requirement. Her experience and skill set make her a 
highly qualified candidate."
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) parser. You will be given a job description 
and a resume. Your job is to find the percentage match between the two, based on the presence 
of required skills, relevant experience (measured in years), matching keywords related to job 
duties, and education level. Return the result as a single number between 0 and 100, followed 
by the percentage sign (%).

Here's an example:

Job Description: "Software Engineer with 3+ years of experience in Java, Spring, and REST APIs.
 Bachelor's degree in Computer Science required."

Resume: "Jane Doe. Software Engineer with 5 years of experience in Java and Spring. Developed 
REST APIs. Bachelor's degree in Computer Science."

Percentage Match: 85% (High skill and experience match, meets education requirements).
"""

input_prompt3 = """
You are an expert recruitment analyst responsible for determining if a candidate is a good match 
for a job description. You will be given the following information about a candidate:

*   Match Percentage: [Insert percentage value (0-100)]
*   Confidence Level: [Insert "High", "Medium", or "Low", or "Not Available" if unknown]
*   Skills Match: [Insert a brief description of how well the candidate's skills align with the job requirements. Examples: "Strong alignment with key skills", "Partial alignment with some skills", "Weak alignment, missing several key skills"]
*   Experience Match: [Insert a brief description of how well the candidate's experience aligns with the job requirements. Examples: "Extensive and highly relevant experience", "Some relevant experience, but not in all areas", "Limited or no relevant experience"]

Your task is to determine whether the candidate is a "Good Match" or a "Bad Match" for the job description.

Here's how you should approach the decision:

1.  **Analyze the Match Percentage:** A percentage of 70% or higher is generally considered a strong match. A percentage below 50% is generally considered a weak match.
2.  **Consider the Confidence Level:** A High confidence level increases the reliability of the percentage match. A Low confidence level decreases the reliability. If the confidence level is "Not Available," give less weight to the percentage match.
3.  **Evaluate the Skills Match:** A "Strong alignment" indicates that the candidate possesses the key skills required for the job. A "Partial alignment" suggests some skills are present, but others are missing. A "Weak alignment" indicates a significant mismatch in skills.
4.  **Evaluate the Experience Match:** "Extensive and highly relevant experience" is a strong indicator of a good match. "Some relevant experience" is a moderate indicator. "Limited or no relevant experience" is a strong indicator of a bad match.
5.  **Make the Decision:** Based on the above analysis, decide whether the candidate is a "Good Match" or a "Bad Match." Use the following guidelines:
    *   If the Match Percentage is 70% or higher AND the Confidence Level is High, then it's a "Good Match".
    *   If the Match Percentage is below 50%, then it's a "Bad Match".
    *   If the Skills Match is "Strong alignment" AND the Experience Match is "Extensive and highly relevant experience", then it's a "Good Match", regardless of the percentage.
    *   If the Skills Match is "Weak alignment" OR the Experience Match is "Limited or no relevant experience", then it's a "Bad Match", regardless of the percentage.
    *   In all other cases, weigh the percentage, confidence level, skills match, and experience match to make a reasoned decision.

6.  **Explain Your Reasoning:** After making the decision, provide a brief explanation of *why* you made that decision, referencing the input features.

For example, if the Match Percentage is 80%, the Confidence Level is High, the Skills Match is "Strong alignment", and the Experience Match is "Extensive and highly relevant experience," you would respond:

"Good Match. The candidate has a high match percentage (80%) with high confidence, strong skills alignment, and extensive relevant experience."
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
