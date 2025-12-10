# Real-Time Q&A Agent 🤖

A web-connected AI chatbot built with Google ADK that provides real-time, accurate answers by searching the web for current information.

## 🌟 Why This Project?

Traditional AI chatbots like ChatGPT and Claude are limited by their training data cutoffs. This agent breaks those limitations by:
- 🔍 **Real-time web search** for current information
- 📊 **Up-to-date data** on news, events, and trends
- 🎯 **Accurate responses** backed by live web sources
- 🚀 **Better performance** for current information queries

## 🔥 Key Features

- **Google ADK Integration**: Powered by Gemini 2.5 Pro
- **Web Search Tool**: Real-time Google search capabilities
- **Streamlit Interface**: Clean, user-friendly web UI
- **Session Management**: Maintains conversation context
- **Async Processing**: Efficient query handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google ADK API access

### Installation & Setup

1. **Download the app file**
   ```bash
   # Download app.py from this repository
   ```

2. **Install required packages**
   ```bash
   pip install streamlit asyncio google-adk python-dotenv
   ```

3. **Set up environment variables**
   Create a `.env` file in the same directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

1. Open your browser to `http://localhost:8501`
2. Ask any question in the input field
3. Get real-time, web-sourced answers instantly!

### Example Queries
- "What are the latest developments in AI?"
- "Current stock price of Tesla"
- "Recent news about climate change"
- "How to plant a papaya tree?"

## 🏗️ How It Works

The app uses Google ADK to create an AI agent that can:
1. Accept user questions through Streamlit interface
2. Search the web in real-time using Google Search tool
3. Process and synthesize information from multiple sources
4. Return accurate, up-to-date responses

## 📊 Performance Advantage

| Feature | Traditional Chatbots | This Agent |
|---------|---------------------|------------|
| Real-time data | ❌ | ✅ |
| Current events | ❌ | ✅ |
| Web search capability | ❌ | ✅ |
| Updated information | ❌ | ✅ |

## 🔧 Technical Stack

- **Backend**: Google ADK, Python
- **Frontend**: Streamlit
- **AI Model**: Gemini 2.5 Pro
- **Search**: Google Search API
- **Styling**: Tailwind CSS

## 📋 Code Structure

The `app.py` file contains:
- Agent definition with Google Search tool
- Async function for agent execution
- Streamlit UI components
- Session management
- Error handling


## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Nageswara Rao Vutla**
- Associate Machine Learning and Generative AI Engineer

## ⭐ Support

If you find this project helpful, please give it a star! ⭐

---

**Built with ❤️ using Google ADK and Streamlit**
