# 📄 ATS Resume Analyzer & Tracker

An AI-powered **Resume Analyzer** that helps you optimize your resume for **Applicant Tracking Systems (ATS)** and tailor it to job descriptions.  
Built with **Streamlit** and **Together AI Llama-3.3-70B**, this app provides **structured feedback** and a **match score** between your resume and job postings.

---

## 🚀 Features

- **Resume Perfection**
  - Upload your resume (PDF).
  - Get detailed feedback on formatting, content, keywords, and ATS compatibility.
  - Receive actionable improvement suggestions.
  - AI provides a **Perfection Score** (Excellent, Good, Needs Improvement, Poor).

- **ATS Match Score**
  - Upload your resume and paste a job description.
  - Get a **percentage match score** between your resume and the job.
  - See detailed keyword analysis (matched vs. missing skills).
  - Understand experience alignment with job requirements.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) - UI framework
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) - PDF text extraction
- [Together AI](https://www.together.ai/) - LLM API (Llama-3.3-70B-Instruct-Turbo)
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment management

---

## 📂 Project Structure

```

ATS-Resume-Analyzer/
│── app.py               # Streamlit application
│── .env                 # API keys (not committed)
│── README.md            # Documentation

````

---

## ⚙️ Installation & Setup

### 3. Install Dependencies

```bash
pip install streamlit pymupdf together python-dotenv
```

### 4. Set Up API Key

Create a `.env` file in the root directory:

```
TOGETHER_API_KEY=your_api_key_here
```

You can get your key from [Together AI](https://api.together.ai/).

### 5. Run the App

```bash
streamlit run app.py
```

---

## 📦 Requirements

`requirements.txt`:

```
streamlit
pymupdf
together
python-dotenv
```

---

## 🎯 Usage

1. **Resume Perfection** tab:

   * Upload your resume PDF.
   * Click **Analyze Resume**.
   * Get structured AI feedback and a Perfection Score.

2. **ATS Match Score** tab:

   * Upload resume + paste job description.
   * Click **Calculate Match Score**.
   * See ATS Match %, keyword analysis, and experience alignment.

---

## ⚠️ Disclaimer

This tool provides **AI-generated suggestions**.
Always review the results manually before applying to jobs.