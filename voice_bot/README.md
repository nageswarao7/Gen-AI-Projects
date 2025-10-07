# 🎙️ AI Voice-to-Text & Chat App (Gemini)

An interactive **Streamlit application** powered by **Google Gemini models** that allows users to **record audio, transcribe speech to text**, and interact with Gemini for intelligent responses.

---

## 🚀 Features

* 🎤 Record voice directly in the browser using the built-in audio recorder
* 🧠 Transcribe speech to text using **Google Gemini models**
* 💬 Chat with the AI model for contextual replies
* ⚡ Fast and simple Streamlit interface

---

## 🧩 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Google Gemini API (`google-genai`)
* **Audio Input:** `audio-recorder-streamlit`

---

## 🛠️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/ai-voice-app.git
   cd ai-voice-app
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## 📁 Requirements

```
streamlit>=1.37.0
google-genai>=0.3.0
audio-recorder-streamlit>=0.0.8
python-dotenv
```

---

## 💡 Usage

1. Click the **Record** button to capture your voice.
2. The app processes the audio and sends it to Gemini for text generation.
3. View the transcription and AI response instantly in the interface.