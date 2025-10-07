import streamlit as st
from google import genai
from google.genai import types
import wave
import io
from audio_recorder_streamlit import audio_recorder


@st.cache_resource
def get_client():
    api_key = st.secrets["GOOGLE_API_KEY"]
    return genai.Client(api_key=api_key)

def wave_file_bytes(pcm, channels=1, rate=24000, sample_width=2):
    """Convert PCM data to WAV bytes"""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    buffer.seek(0)
    return buffer.read()

def speech_to_text(client, audio_bytes):
    """Convert speech to text using Gemini"""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            'Convert speech to text accurately',
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type='audio/wav',
            )
        ]
    )
    return response.text

def generate_personalized_response(client, question):
    """Generate response based on Nageswara Rao's profile"""
    
    # Your complete personal context
    context = """
    You are Nageswara Rao Vutla, and you should answer questions as yourself in first person.
    
    PERSONAL BACKGROUND:
    - Full Name: Nageswara Rao Vutla
    - Location: Currently in Hyderabad, Telangana, India
    - Hometown: Grew up in Medapi, Andhra Pradesh
    - Contact: nageswararaovutla7@gmail.com | +91 8466091561
    
    CURRENT ROLE:
    - Position: Associate ML & Generative AI Engineer at Quixy
    - Started: February 2025 (previously intern from July 2024 - Jan 2025)
    - Total Experience: 1+ years in ML/AI
    
    EDUCATION:
    - B.Tech in Mechanical Engineering from Bapatla Engineering College (Apr 2023) - CGPA: 8.27
    - Diploma in Mechanical Engineering from GIET, Rajahmundry (Apr 2020) - 79.88%
    - Transitioned from Mechanical Engineering to AI/ML through self-learning and passion
    
    TECHNICAL EXPERTISE:
    Core Strengths:
    - LLMs, NLP, Generative AI, Computer Vision, Deep Learning
    - Agentic AI systems (Google ADK, CrewAI, LangGraph, AutoGen)
    - RAG systems (Semantic, Hybrid, Graph-based with Neo4j)
    - Fine-tuning, Quantization, LoRA, QLoRA
    - Multi-agent systems and workflow automation
    
    Technologies:
    - Languages: Python, SQL
    - LLM Frameworks: LangChain, LlamaIndex, CrewAI, LangGraph, Google ADK
    - Vector DBs: ChromaDB, FAISS, Pinecone, Qdrant, Neo4j
    - LLMs: GPT-4o, Claude-3.5, Gemini 2.5, Llama, Mistral
    - Deployment: FastAPI, Flask, Streamlit, Docker, CI/CD
    - Tools: Claude CLI, Gemini CLI
    
    KEY ACHIEVEMENTS:
    1. Won Agentic AI Hackathon at Quixy for AI Recruitment System
    2. Led multi-agent forecasting system cutting runtime by 60% and boosting accuracy by 12%
    3. Built AI-powered analytics dashboard with NL-to-SQL conversion
    4. Developed Neo4j-based Agentic RAG system with Cypher queries
    5. Created AI Recruitment Assistant reducing hiring time by 35%
    6. Built AgriBharat - AI Assistant for Indian farmers
    7. Developed Number Plate Detection system with 87% accuracy
    
    RECENT PROJECTS:
    - Multi-agent forecasting system (Google ADK + Gemini 2.5 Pro)
    - AI Recruitment Assistant (CrewAI + Whisper + Aadhaar verification)
    - Neo4j Agentic RAG (Gemini 2.5 + ChromaDB + LangChain)
    - SRS-to-JSON automation (GPT-4o + LangChain)
    - AgriBharat farmer assistant
    
    YOUR PERSONALITY & WORK STYLE:
    - Passionate about solving real-world problems with AI
    - Quick learner who transitioned from Mechanical to AI/ML
    - Hands-on builder who loves experimenting with cutting-edge tech
    - Team player who won hackathons and collaborates well
    - Detail-oriented with focus on production-ready solutions
    - Enthusiastic about agentic AI and multi-agent systems
    
    YOUR SUPERPOWER:
    - Rapid prototyping and turning ideas into working AI systems
    - Building complex multi-agent systems that automate workflows
    - Bridge between theory and practical deployment
    
    AREAS TO GROW:
    - Advanced MLOps and production scaling at enterprise level
    - Deeper understanding of distributed systems architecture
    - Leadership and mentoring skills
    - Cloud infrastructure optimization (AWS, GCP)
    - Research paper publication
    
    MISCONCEPTIONS COWORKERS MIGHT HAVE:
    - They might think you're only theoretical because of strong technical knowledge, but you're very hands-on
    - Some might underestimate your experience because you're relatively new, but you've delivered production systems
    - Coming from Mechanical background, some might doubt AI depth, but you've proven expertise through projects
    
    HOW YOU PUSH BOUNDARIES:
    - Constantly experiment with latest AI tools (Claude CLI, Gemini CLI, Google ADK)
    - Participate in hackathons and win them
    - Build personal projects (AgriBharat) to learn new technologies
    - Take on complex challenges like Neo4j RAG and multi-agent systems
    - Self-taught transition from Mechanical to AI shows determination
    
    Question: {question}
    
    INSTRUCTIONS:
    - Answer in first person as Nageswara Rao
    - Be authentic, confident but humble
    - Use specific examples from your experience
    - Keep it conversational (2-4 sentences)
    - Show enthusiasm for AI/ML
    - Mention your journey from Medapi, Andhra Pradesh when relevant
    - Reference specific projects or achievements that relate to the question
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context.format(question=question)
    )
    return response.text

def text_to_speech(client, text):
    """Convert text to speech using Gemini TTS"""
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=f"Say in a friendly, confident, and professional tone: {text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Orus',
                    )
                )
            ),
        )
    )
    
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    return wave_file_bytes(audio_data)

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Voice Bot - Nageswara Rao Vutla",
        page_icon="🎤",
        layout="centered"
    )
    
    # Header
    st.title("🎤 Voice Bot - Nageswara Rao Vutla")
    st.markdown("**Associate ML & Generative AI Engineer @ Quixy**")
    st.markdown("*Hyderabad, Telangana | From Medapi, Andhra Pradesh*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("📧 nageswararaovutla7@gmail.com")
    with col2:
        st.markdown("📱 +91 8466091561")
    with col3:
        st.markdown("🏆 Hackathon Winner")
    
    st.divider()
    
    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    client = get_client()
    
    # Main interaction area
    st.markdown("### 🎙️ Ask me anything!")
    st.markdown("Record your question or type below:")
    st.write("Click the **microphone button** below to start recording. Click it again to stop. Once stopped, your audio will be processed automatically.")

    audio_bytes = audio_recorder(
        text="🎙️ Click to start or stop recording",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x",
        key="audio_recorder"
    )

    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        with st.spinner("🎧 Processing your question..."):
            try:
                # Speech to text
                question = speech_to_text(client, audio_bytes)
                st.success(f"**You asked:** {question}")
                
                # Generate response
                with st.spinner("🤔 Thinking..."):
                    answer = generate_personalized_response(client, question)
                    st.info(f"**My response:** {answer}")
                
                # Text to speech
                with st.spinner("🔊 Generating voice response..."):
                    audio_response = text_to_speech(client, answer)
                    st.audio(audio_response, format="audio/wav")
                    st.success("✅ Response complete!")
                
                # Save to history
                st.session_state.conversation_history.append({
                    'question': question,
                    'answer': answer,
                    'audio': audio_response
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please try again or use the text input below.")
    
    # Text input option
    st.divider()
    st.markdown("### ⌨️ Or type your question:")
    
    with st.form("text_form"):
        text_question = st.text_area(
            "Type your question here",
            height=100,
            placeholder="e.g., What should we know about your life story?"
        )
        submitted = st.form_submit_button("🚀 Ask", type="primary", use_container_width=True)
    
    if submitted and text_question:
        with st.spinner("🤔 Thinking..."):
            try:
                answer = generate_personalized_response(client, text_question)
                st.info(f"**My response:** {answer}")
                
                with st.spinner("🔊 Generating voice response..."):
                    audio_response = text_to_speech(client, answer)
                    st.audio(audio_response, format="audio/wav")
                    st.success("✅ Response complete!")
                
                st.session_state.conversation_history.append({
                    'question': text_question,
                    'answer': answer,
                    'audio': audio_response
                })
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Conversation history
    if st.session_state.conversation_history:
        st.divider()
        st.markdown("### 💬 Conversation History")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history)):
            with st.expander(f"Q{len(st.session_state.conversation_history)-i}: {conv['question'][:60]}...", expanded=(i==0)):
                st.markdown(f"**❓ Question:** {conv['question']}")
                st.markdown(f"**💡 Answer:** {conv['answer']}")
                if 'audio' in conv:
                    st.audio(conv['audio'], format="audio/wav")
        
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Sample questions sidebar
    with st.sidebar:
        st.markdown("## 📝 Sample Questions")
        st.markdown("""
        Try asking me:
        
        **About Me:**
        - What should we know about your life story in a few sentences?
        - Tell me about your journey from Medapi to Hyderabad
        - How did you transition from Mechanical to AI/ML?
        
        **Skills & Strengths:**
        - What's your #1 superpower?
        - What are your core technical strengths?
        - Tell me about your experience with multi-agent systems
        
        **Growth & Development:**
        - What are the top 3 areas you'd like to grow in?
        - What technologies are you currently learning?
        - Where do you see yourself in 2 years?
        
        **Work Style:**
        - What misconception do your coworkers have about you?
        - How do you approach complex AI problems?
        - Describe your work style in 3 words
        
        **Achievements:**
        - How do you push your boundaries and limits?
        - Tell me about your hackathon win
        - What's your most impactful project?
        - Tell me about AgriBharat project
        
        **Technical Deep Dive:**
        - Explain your Neo4j RAG system
        - How did you reduce hiring time by 35%?
        - What's your experience with Google ADK?
        """)
        
        st.divider()
        st.markdown("### 🔗 Links")
        st.markdown("""
        - [LinkedIn](https://www.linkedin.com/in/nageswara-rao-vutla/)
        - [GitHub](https://github.com/nageswarao7?tab=repositories)
        - [Medium](https://nageswararaovutla7.medium.com/)
        """)
        
        st.divider()
        st.markdown("### 🛠️ Tech Stack Highlights")
        st.markdown("""
        - **LLMs:** GPT-4o, Claude-3.5, Gemini 2.5
        - **Frameworks:** LangChain, CrewAI, LangGraph, Google ADK
        - **Databases:** ChromaDB, Neo4j, FAISS
        - **Deployment:** FastAPI, Docker, CI/CD
        """)

if __name__ == "__main__":
    main()