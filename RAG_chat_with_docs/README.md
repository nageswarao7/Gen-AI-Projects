# 📄🤖 RAG App – Chat with Your Documents & URLs

This is a **Retrieval-Augmented Generation (RAG) application** built with **Streamlit**.
It lets you upload **PDFs** and fetch content from **URLs**, stores them in a vector database (**ChromaDB**), and allows you to **chat with your documents** using **Together AI’s LLMs**.

---

## 🚀 Features

* 📚 Upload and process **PDF documents**
* 🌐 Scrape and embed text from **URLs**
* 🧩 **Text chunking & embeddings** with `sentence-transformers`
* 💾 Store vectors in a **persistent ChromaDB database**
* 🔍 **Semantic search** for relevant context
* 🤖 **LLM-powered answers** using Together AI (`meta-llama/Llama-3-8b-chat-hf`)
* 💬 Simple **chat interface** with conversation history

---

## 📦 Installation

1. **Install dependencies directly**

   ```bash
   pip install streamlit chromadb sentence-transformers pypdf beautifulsoup4 together requests python-dotenv
   ```

2. **Set up environment variables**
   Create a `.env` file in the project root with your Together API key:

   ```
   TOGETHER_API_KEY=your_api_key_here
   ```

---

## ▶️ Usage

Run the app with:

```bash
streamlit run app.py
```

### Workflow:

1. Upload one or more **PDF files** or paste **URLs** in the sidebar.
2. Click **Process Documents & URLs** to embed them into ChromaDB.
3. Ask a question in the chat box.
4. The app retrieves relevant context and generates an **LLM-powered answer**.

---

## 📂 Project Structure

```
RAG_chat_with_docs/
│── app.py       # Main Streamlit application
│── .env         # Your API key (not committed)
│── README.md    # Documentation
```

---

## ✅ Example `.env` File

```
TOGETHER_API_KEY=your_api_key_here
```

---

## 🙌 Credits

* [Streamlit](https://streamlit.io/)
* [ChromaDB](https://docs.trychroma.com/)
* [SentenceTransformers](https://www.sbert.net/)
* [Together AI](https://www.together.ai/)
