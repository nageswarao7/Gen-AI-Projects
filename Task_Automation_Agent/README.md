# 🤖 Task Automation Agent

A **Streamlit-based AI assistant** powered by **LangChain** and **Together AI (Llama-3-70B)**.
This agent can:

* 🔍 **Search** current events, weather, and facts (via Google Serper API)
* 📝 **Save notes** to a file (`notes.txt`)
* 📄 **Summarize PDFs** uploaded through the UI
* 💬 **Chat naturally** for general queries and conversations

---

## 🚀 Features

* **LangChain ReAct Agent** with custom prompt
* **Multiple tools**: Web Search, Write Note, PDF Summarization
* **Overwrites notes** when saving (no duplicates)
* **Download button** for saved notes
* **Clean Streamlit chat UI** with persistent chat history

---

## 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/) – UI framework
* [LangChain](https://www.langchain.com/) – Agent + tools
* [Together AI](https://www.together.ai/) – LLM inference (`meta-llama/Llama-3-70b-chat-hf`)
* [Google Serper API](https://serper.dev/) – Web search
* [PyPDFLoader](https://python.langchain.com/docs/integrations/document_loaders/pypdf) – PDF parsing
* [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management

---

## 📦 Installation


1. **Install dependencies**

   ```bash
   pip install streamlit langchain langchain-together langchain-community python-dotenv pypdf
   ```

2. **Set up environment variables**
   Create a `.env` file in the project root:

   ```
   TOGETHER_API_KEY=your_together_api_key_here
   SERPER_API_KEY=your_google_serper_api_key_here
   ```

---

## ▶️ Usage

Run the app with:

```bash
streamlit run app.py
```

### Example Commands

* **Search**:

  ```
  What’s the temperature in Hyderabad?
  ```
* **Save Note**:

  ```
  save note: Buy groceries tomorrow at 6 PM
  ```
* **Summarize PDF**:
  Upload a PDF in the sidebar and then ask:

  ```
  Summarize the PDF
  ```

---

## 📂 Project Structure

```
Task_Automation_Agent/
│── app.py          # Main Streamlit application
│── .env            # Environment variables (not committed)
│── README.md       # Documentation
│── notes.txt       # Auto-generated when saving notes
```

---

## ✅ Example `.env` File

```
TOGETHER_API_KEY=your_together_api_key_here
SERPER_API_KEY=your_google_serper_api_key_here
```

---

## 🙌 Credits

* [LangChain](https://www.langchain.com/)
* [Together AI](https://www.together.ai/)
* [Google Serper](https://serper.dev/)
* [Streamlit](https://streamlit.io/)