# Key aspects of the problem:
1. **Extracting job requirements**: Parse job descriptions to identify required skills (e.g., Python, Java, SQL), experience level (e.g., 2+ years), education (e.g., Bachelor's in CS), and other qualifications.
2. **Feature Extraction**: Extract information from resumes (PDFs) to identify candidates' skills, experience, and qualifications.
3. **Matching Algorithm**: Use NLP and machine learning techniques(e.g., LLMs, Word2Vec) to compare resume content with job requirements.
4. **Filtering**: Give a percentage score to each resume based on the provided job description and classifying into “good match” or a “bad match”.

# Proposed Solution:
1. **Data Acquisition and preprocessing:**
   * User Inputs - the job description is provided as free text in a text box, whereas the resume upload is accepted in PDF format.
   * Resume parsing - Use PyPDF2 to extract text from the uploaded resume, and perform very basic text preprocessing.
2. **Feature extraction:**
   * Tokenization & Stopword Removal – Break text into meaningful words.
   * Word Embeddings (BERT/Gemini API) – Capture contextual meaning.
   * Named Entity Recognition (NER) – Extract skills, experience, education from resumes.
3. **Resume Evaluation:**
   * Resume summary prompt - Extracts key information from the resume. Summarizes qualifications and experience in relation to the job description.
   * Percentage match prompt - Analyzes the similarity between the resume and the job description. Returns a match percentage based on relevance.
   * Good/Bad Match Classification Prompt - Determines whether the candidate is a "Good Match" or "Bad Match." Considers skills, experience, and match percentage in the evaluation.
4. **Displaying results in Streamlit UI**: The extracted resume text is analyzed using Google Gemini API, and the response is displayed.

# Workflow Diagram:
