# 🎨 AI Image Generator & Editor

An interactive **Streamlit application** powered by **Google Gemini models** that allows you to:

* 🖼️ **Generate AI images** from text prompts
* ✂️ **Edit uploaded images** using AI instructions
* 🔎 **Ask questions about images** (Image Q\&A)

---

## 🚀 Features

✅ Generate high-quality AI images from text prompts
✅ Edit existing images with natural language instructions
✅ Ask questions about uploaded images (e.g., "Caption this image")
✅ Download generated/edited images
✅ User-friendly Streamlit interface

---

## 📂 Project Structure

```
AI_Image_Studio/
│── app.py              # Main Streamlit app
│── README.md           # Project documentation
│── .env                # Store your API key (not committed to Git)
```

---

## 🛠️ Requirements

Create a virtual environment and install dependencies:

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

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open the local URL in your browser (default: `http://localhost:8501`).

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
