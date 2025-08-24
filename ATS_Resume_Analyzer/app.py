import streamlit as st
import fitz  # PyMuPDF
import os
from together import Together
from dotenv import load_dotenv

# --- SETUP ---
# Load environment variables from .env file
try:
    load_dotenv()
    # It's recommended to set the API key as an environment variable
    # for security. Name it TOGETHER_API_KEY in your .env file.
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
except ImportError:
    st.error("The 'python-dotenv' package is not installed. Please install it using 'pip install python-dotenv'")
    client = None
except Exception as e:
    st.error(f"Could not initialize the Together client. Make sure your API key is set in a .env file as TOGETHER_API_KEY. Error: {e}")
    client = None


# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    """
    if pdf_file is not None:
        try:
            # To read the file in memory, we use getvalue()
            pdf_bytes = pdf_file.getvalue()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
    return None

def get_llm_response(prompt, system_prompt):
    """
    Sends a prompt to the Together AI model and gets a response.
    """
    if not client:
        st.error("Together AI client is not initialized. Cannot process the request.")
        return "Error: Client not initialized."
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while communicating with the AI model: {e}")
        return f"Error: {e}"


# --- STREAMLIT APP LAYOUT ---

st.set_page_config(page_title="ATS Resume Tracker", layout="wide")
st.title("📄 ATS Resume Tracker & Analyzer")
st.markdown("Optimize your resume for Applicant Tracking Systems (ATS) and improve its quality.")

# Create two tabs
tab1, tab2 = st.tabs(["📝 Resume Perfection", "🎯 ATS Match Score"])

# --- TAB 1: RESUME PERFECTION ---
with tab1:
    st.header("Analyze and Refine Your Resume")
    st.markdown("Upload your resume in PDF format to receive feedback on its strengths and weaknesses. The AI will provide suggestions for improvement.")

    uploaded_resume_perfection = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="perfection_uploader")

    if st.button("Analyze Resume", key="analyze_button"):
        if uploaded_resume_perfection is not None:
            with st.spinner("Extracting text from resume..."):
                resume_text = extract_text_from_pdf(uploaded_resume_perfection)
                print(resume_text)
            if resume_text:
                st.success("Resume text extracted successfully!")
                with st.spinner("AI is analyzing your resume... This may take a moment."):
                    system_prompt_perfection = """
                    You are an expert career coach and professional resume writer. 
                    Your task is to review the provided resume text and deliver structured, constructive feedback.

                    You must perform the following:

                    1. **Clarity & Impact:** 
                    - Assess whether the resume clearly communicates the candidate’s skills, achievements, and career trajectory.
                    - Comment on the strength and action-orientation of bullet points and descriptions.

                    2. **ATS Compatibility:** 
                    - Evaluate formatting, keyword usage, and structure for ATS readability.
                    - Identify missing or weak keywords relevant to modern job descriptions.

                    3. **Strengths & Weaknesses Summary:** 
                    - Highlight what the resume does well. 
                    - Point out areas that weaken its effectiveness.

                    4. **Specific, Actionable Suggestions:** 
                    - Organize your feedback under clear sections: 
                        - *Formatting*
                        - *Content*
                        - *Keywords*
                        - *Achievements/Impact*
                        - *Experience & Consistency*
                    - Provide concrete recommendations for each.

                    5. **Final Evaluation:** 
                    - Conclude with an overall "Perfection Score" (Excellent, Good, Needs Improvement, Poor). 
                    - Add a brief, encouraging closing remark.

                    Your response must be professional, structured, and highly actionable. 
                    Do not be conversational; focus on objective, career-focused feedback.
                    """

                    user_prompt_perfection = f"Please review the following resume and provide feedback:\n\n---\n\n{resume_text}"

                    response = get_llm_response(user_prompt_perfection, system_prompt_perfection)

                    st.subheader("AI Feedback on Your Resume")
                    st.markdown(response)
        else:
            st.warning("Please upload a resume PDF file first.")

# --- TAB 2: ATS MATCH SCORE ---
with tab2:
    st.header("Calculate Resume-to-Job Description Match Score")
    st.markdown("Upload your resume and paste the job description to see how well you match the requirements. This helps in tailoring your resume for specific job applications.")

    uploaded_resume_ats = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="ats_uploader")
    job_description = st.text_area("Paste the Job Description Here", height=300, key="jd_input")

    if st.button("Calculate Match Score", key="match_button"):
        if uploaded_resume_ats is not None and job_description:
            with st.spinner("Processing..."):
                resume_text = extract_text_from_pdf(uploaded_resume_ats)
                print(resume_text)
                if resume_text:
                    system_prompt_ats = """
                    You are a highly sophisticated Applicant Tracking System (ATS). 
                    Your function is to analyze a resume against a given job description.

                    Your main goal is to calculate a percentage match score based on how well the resume's 
                    skills, years of experience, and qualifications align with the job requirements.

                    You must provide the following in your response:

                    1. **Percentage Match Score:** A single percentage value (e.g., "85%"). 
                    The score must consider both skills/keywords alignment and the relevance of total years of experience compared to the job description.

                    2. **Detailed Analysis:** 
                    - Explain the reasoning behind the score. 
                    - Highlight skills, tools, and qualifications that match the job description. 
                    - Point out gaps in required skills, tools, or qualifications. 
                    - Explicitly compare the candidate’s years of experience with the years required in the job description (if specified).

                    3. **Keywords Analysis:** 
                    - Extract crucial keywords from the job description. 
                    - Indicate whether each keyword was found in the resume. 
                    - Note the strength of match where applicable (e.g., "Python – 5 years (requirement: 3 years)").

                    The analysis must be structured, data-driven, and non-conversational.
                    """

                    user_prompt_ats = f"""
                    **RESUME:**
                    {resume_text}

                    ---

                    **JOB DESCRIPTION:**
                    {job_description}
                    """

                    response_ats = get_llm_response(user_prompt_ats, system_prompt_ats)

                    st.subheader("ATS Analysis Result")
                    st.markdown(response_ats)
        else:
            st.warning("Please upload a resume and provide a job description.")

# --- SIDEBAR ---
st.sidebar.title("About")
st.sidebar.info(
    "This application uses AI to help you improve your resume and tailor it for job applications. "
    "It is powered by Streamlit and the Together AI platform."
)
st.sidebar.title("How to Use")
st.sidebar.markdown(
    """
    **Resume Perfection:**
    1.  Go to the 'Resume Perfection' tab.
    2.  Upload your resume in PDF format.
    3.  Click 'Analyze Resume'.
    4.  Review the AI-generated feedback.

    **ATS Match Score:**
    1.  Go to the 'ATS Match Score' tab.
    2.  Upload your resume.
    3.  Paste the target job description into the text box.
    4.  Click 'Calculate Match Score'.
    """
)
st.sidebar.warning("Note: This is an AI-powered tool. Always double-check the feedback and use your best judgment.")
