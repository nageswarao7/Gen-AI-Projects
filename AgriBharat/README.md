# 🌾 AgriBharat - AI-Powered Agricultural Assistant

AgriBharat is a comprehensive, AI-driven application designed to empower Indian farmers with real-time insights, disease diagnosis, market trends, and government scheme information. Built with **Streamlit** and powered by **Google Gemini**, it offers a multi-lingual, voice-enabled interface tailored for accessibility.

## 🚀 Features

- **🌾 Crop Queries**: Ask questions about crop management, soil health, and best practices via text or voice.
- **🌿 Disease Diagnosis**: Upload images of plant leaves to identify diseases, get treatment recommendations, and precautions.
- **💰 Market Analysis**: Get real-time market trends, price information, and demand/supply data for specific crops.
- **📄 Government Schemes**: Discover relevant government schemes, subsidies, and eligibility criteria.
- **☁️ Weather Forecast**: Access current weather conditions and 3-day forecasts for any location in India.
- **🗣️ Multi-Lingual & Voice Support**: Full support for **English, Hindi, Telugu, Kannada, Malayalam, and Tamil**, with Speech-to-Text and Text-to-Speech capabilities.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Models**: [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) (Text & Vision), Gemini TTS/STT
- **Language**: Python 3.x
- **Search**: Google Search Tool (via Google ADK)

## 📋 Prerequisites

- Python 3.9 or higher
- A Google Cloud Project with Gemini API access
- An API Key for Google GenAI

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/nageswarao7/Gen-AI-Projects.git
    cd AgriBharat
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install key packages manually: `streamlit`, `google-genai`, `python-dotenv`, `google-adk`)*

4.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    ```

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`.

## 📂 Project Structure

- `main.py`: The main entry point for the Streamlit application, handling UI and user interaction.
- `core.py`: Contains the core logic, including agent definitions (QA, Vision, Market, Schemes, Weather) and execution flows.
- `translations.py`: Dictionary containing UI text translations for all supported languages.
- `styles.py`: Custom CSS for the "Natural Elegance" UI theme.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[MIT License](LICENSE)
