# 🎨 AI Image Studio

An interactive **Streamlit application** powered by **Google Gemini models** that lets you:

* 🖼️ **Generate AI images** from text prompts
* ✂️ **Edit uploaded images** with natural language instructions
* 🔎 **Ask questions about images** (Image Q\&A)

---

## 🚀 Features

✅ Generate high-quality AI images from descriptive prompts
✅ Edit uploaded images using AI-based modifications
✅ Ask questions about uploaded images (e.g., *"What is in this picture?"* or *"Caption this image"*)
✅ Download generated or edited images
✅ Clean and responsive **Streamlit UI** with custom styling

---

## 📂 Project Structure

```
AI_Image_Studio/
│── app.py              # Main Streamlit UI
│── core.py             # Core logic for image generation, editing & Q&A
│── .env                # Store your API key (not committed to Git)
│── README.md           # Project documentation
```

---

## 🛠️ Installation & Requirements

Create and activate a virtual environment, then install dependencies:

```bash
pip install streamlit python-dotenv pillow google-genai
```

---

## 🔑 Setup

1. Get your **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.env` file in the project root and add:

```bash
GOOGLE_API_KEY=your_api_key_here
```

⚠️ **Do not hardcode your API key** inside the code. Always load it from `.env`.

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open the local URL in your browser (default: `http://localhost:8501`).

---

## 📌 Example Usage

* **Image Generation:**
  Prompt → *"A 3D rendered pig with wings and a top hat flying over a futuristic city"*

* **Image Editing:**
  Instruction → *"Add a llama next to me"*

* **Image Q\&A:**
  Query → *"Caption this image"*

---

## 📜 License

This project is licensed under the **MIT License**.

