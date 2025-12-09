import streamlit as st
import asyncio
import io
import wave
from google import genai
from google.genai import types
from core import run_qa_agent, run_comprehensive_disease_analysis, run_market_analysis, run_government_schemes, run_weather_forecast
from translations import translations
from styles import natural_elegance

# --- Initialize Gemini Client ---
@st.cache_resource
def get_gemini_client():
    return genai.Client()

# --- Speech to Text Function ---
def speech_to_text(audio_bytes, mime_type='audio/wav'):
    """Convert audio bytes to text using Gemini"""
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                'Convert this audio into text. Only return the transcribed text without any additional explanation.',
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type,
                )
            ]
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Speech-to-text error: {str(e)}")
        return None

# --- Text to Speech Function ---
def text_to_speech(text, language="English"):
    """Convert text to speech using Gemini and return audio bytes"""
    try:
        client = get_gemini_client()
        
        # Select voice based on language
        voice_map = {
            "English": "Kore",
            "Hindi": "Puck",
            "Telugu": "Kore",
            "Kannada": "Kore",
            "Malayalam": "Kore",
            "Tamil": "Kore"
        }
        
        voice_name = voice_map.get(language, "Kore")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            )
        )
        
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_data)
        
        wav_buffer.seek(0)
        return wav_buffer.read()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="AgriBharat",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- THE "NATURAL ELEGANCE" UI MAKEOVER ---
st.markdown(natural_elegance, unsafe_allow_html=True)

# Initialize session state
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"
if 'consultation_history' not in st.session_state:
    st.session_state.consultation_history = []

# Language selection in sidebar
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center;'>{translations[st.session_state.selected_language]['settings_header']}</h2>", unsafe_allow_html=True)
    language = st.selectbox(
        label=translations[st.session_state.selected_language]["select_language"],
        options=["English", "Hindi", "Telugu", "Kannada", "Malayalam", "Tamil"],
        key="language_select_unique",
        index=["English", "Hindi", "Telugu", "Kannada", "Malayalam", "Tamil"].index(st.session_state.selected_language),
        label_visibility="collapsed"
    )
    
    if language != st.session_state.selected_language:
        st.session_state.selected_language = language
        st.rerun()

# Get translations
t = translations[st.session_state.selected_language]

# --- App Title and Subtitle ---
st.markdown(f"""
    <div class="main-title">
        <span style="font-size: 2.8rem; margin-right: 1rem;">🌾</span>
        <h1>{t['title']}</h1>
        <span style="font-size: 2.8rem; margin-left: 1rem;">🚜</span>
    </div>
    <p class="subtitle">{t['subtitle']}</p>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"🌾 {t['text_query_tab']}",
    f"🌿 {t['image_analysis_tab']}",
    f"💰 {t['market_analysis_tab']}",
    f"📄 {t['government_schemes_tab']}",
    f"☁️ {t['weather_tab']}"
])

# --- Crop Queries Tab ---
with tab1:
    st.markdown(f"<h2 class='section-header'>{t['text_query_title']}</h2>", unsafe_allow_html=True)
    
    # Audio input option
    st.markdown("### 🎤 Voice Input (Optional)")
    audio_input = st.audio_input("Record your question", key="audio_crop_query")
    
    with st.form(key="text_query_form"):
        user_question = st.text_area(label=t["text_input_label"], placeholder=t["text_input_placeholder"], key="text_query_input", height=120)
        submit_button = st.form_submit_button(label=t["submit_button"])

    # Process audio input if provided
    if audio_input and not submit_button:
        with st.spinner("🎤 Converting speech to text..."):
            audio_bytes = audio_input.read()
            transcribed_text = speech_to_text(audio_bytes, mime_type='audio/wav')
            if transcribed_text:
                st.session_state.transcribed_crop_query = transcribed_text
                st.success(f"📝 Transcribed: {transcribed_text}")
                st.info("👆 Click Submit to process this question")

    if submit_button:
        # Use transcribed text if available, otherwise use typed text
        final_question = st.session_state.get('transcribed_crop_query', user_question)
        
        if not final_question.strip():
            st.error(f"{t['error_prefix']} {t['no_question_error']}")
        else:
            with st.spinner(t["processing_question"]):
                try:
                    response = asyncio.run(run_qa_agent(final_question, st.session_state.selected_language))
                    
                    # Display text response
                    st.markdown(f"""<div class="response-card"><h3>{t['response_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    
                    # Generate audio response
                    with st.spinner("🔊 Generating audio response..."):
                        audio_response = text_to_speech(response, st.session_state.selected_language)
                        if audio_response:
                            st.audio(audio_response, format='audio/wav')
                    
                    st.session_state.consultation_history.append({
                        "type": "crop_query", 
                        "question": final_question, 
                        "response": response, 
                        "language": st.session_state.selected_language
                    })
                    
                    # Clear transcribed text
                    if 'transcribed_crop_query' in st.session_state:
                        del st.session_state.transcribed_crop_query
                        
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Disease Diagnosis Tab ---
with tab2:
    st.markdown(f"<h2 class='section-header'>{t['image_analysis_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['image_analysis_subtitle']}</p>", unsafe_allow_html=True)
    
    # Audio input option
    st.markdown("### 🎤 Voice Input (Optional)")
    audio_input_disease = st.audio_input("Record your question about the plant", key="audio_disease_query")
    
    with st.form(key="image_analysis_form"):
        uploaded_image = st.file_uploader(label=t["image_upload_label"], type=["jpg", "jpeg", "png"], key="image_upload_unique")
        image_question = st.text_input(label=t["image_question_label"], placeholder=t["image_question_placeholder"], key="image_question_input")
        submit_image_button = st.form_submit_button(label=t["analyze_button"])

    # Process audio input if provided
    if audio_input_disease and not submit_image_button:
        with st.spinner("🎤 Converting speech to text..."):
            audio_bytes = audio_input_disease.read()
            transcribed_text = speech_to_text(audio_bytes, mime_type='audio/wav')
            if transcribed_text:
                st.session_state.transcribed_disease_query = transcribed_text
                st.success(f"📝 Transcribed: {transcribed_text}")
                st.info("👆 Click Analyze to process this question")

    if submit_image_button:
        if not uploaded_image:
            st.error(f"{t['error_prefix']} {t['no_image_error']}")
        else:
            # Use transcribed text if available, otherwise use typed text
            final_question = st.session_state.get('transcribed_disease_query', image_question if image_question else t["image_question_placeholder"])
            
            with st.spinner(t["processing_image"]):
                try:
                    image_data = uploaded_image.read()
                    response = asyncio.run(run_comprehensive_disease_analysis(
                        image_data=image_data, 
                        user_question=final_question, 
                        language=st.session_state.selected_language
                    ))
                    
                    st.image(uploaded_image, caption=t["uploaded_image_caption"], use_container_width=True)
                    
                    # Display text response
                    st.markdown(f"""<div class="response-card"><h3>{t['analysis_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    
                    # Generate audio response
                    with st.spinner("🔊 Generating audio response..."):
                        audio_response = text_to_speech(response, st.session_state.selected_language)
                        if audio_response:
                            st.audio(audio_response, format='audio/wav')
                    
                    st.session_state.consultation_history.append({
                        "type": "disease_analysis", 
                        "question": final_question, 
                        "response": response, 
                        "language": st.session_state.selected_language
                    })
                    
                    # Clear transcribed text
                    if 'transcribed_disease_query' in st.session_state:
                        del st.session_state.transcribed_disease_query
                        
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Market Analysis Tab ---
with tab3:
    st.markdown(f"<h2 class='section-header'>{t['market_analysis_header']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['market_analysis_subtitle']}</p>", unsafe_allow_html=True)
    
    # Audio input option
    st.markdown("### 🎤 Voice Input (Optional)")
    audio_input_market = st.audio_input("Record the crop name", key="audio_market_query")
    
    with st.form(key="market_analysis_form"):
        crop_name = st.text_input(label=t["crop_name_label"], placeholder=t["crop_name_placeholder"], key="crop_name_input")
        submit_market_button = st.form_submit_button(label=t["get_market_trends_button"])

    # Process audio input if provided
    if audio_input_market and not submit_market_button:
        with st.spinner("🎤 Converting speech to text..."):
            audio_bytes = audio_input_market.read()
            transcribed_text = speech_to_text(audio_bytes, mime_type='audio/wav')
            if transcribed_text:
                st.session_state.transcribed_market_query = transcribed_text
                st.success(f"📝 Transcribed: {transcribed_text}")
                st.info("👆 Click Submit to get market trends")

    if submit_market_button:
        # Use transcribed text if available, otherwise use typed text
        final_crop_name = st.session_state.get('transcribed_market_query', crop_name)
        
        if not final_crop_name.strip():
            st.error(f"{t['error_prefix']} {t['no_crop_name_error']}")
        else:
            with st.spinner(t["processing_market"]):
                try:
                    response = asyncio.run(run_market_analysis(
                        crop_name=final_crop_name, 
                        language=st.session_state.selected_language
                    ))
                    
                    # Display text response
                    st.markdown(f"""<div class="response-card"><h3>{t['market_trends_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    
                    # Generate audio response
                    with st.spinner("🔊 Generating audio response..."):
                        audio_response = text_to_speech(response, st.session_state.selected_language)
                        if audio_response:
                            st.audio(audio_response, format='audio/wav')
                    
                    st.session_state.consultation_history.append({
                        "type": "market_analysis", 
                        "question": f"Market trends for {final_crop_name}", 
                        "response": response, 
                        "language": st.session_state.selected_language
                    })
                    
                    # Clear transcribed text
                    if 'transcribed_market_query' in st.session_state:
                        del st.session_state.transcribed_market_query
                        
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Government Schemes Tab ---
with tab4:
    st.markdown(f"<h2 class='section-header'>{t['government_schemes_header']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['government_schemes_subtitle']}</p>", unsafe_allow_html=True)
    
    # Audio input option
    st.markdown("### 🎤 Voice Input (Optional)")
    audio_input_schemes = st.audio_input("Record your question about schemes", key="audio_schemes_query")
    
    with st.form(key="schemes_form"):
        scheme_query = st.text_input(label=t["scheme_query_label"], placeholder=t["scheme_query_placeholder"], key="scheme_query_input")
        submit_scheme_button = st.form_submit_button(label=t["get_schemes_button"])

    # Process audio input if provided
    if audio_input_schemes and not submit_scheme_button:
        with st.spinner("🎤 Converting speech to text..."):
            audio_bytes = audio_input_schemes.read()
            transcribed_text = speech_to_text(audio_bytes, mime_type='audio/wav')
            if transcribed_text:
                st.session_state.transcribed_schemes_query = transcribed_text
                st.success(f"📝 Transcribed: {transcribed_text}")
                st.info("👆 Click Submit to get schemes information")

    if submit_scheme_button:
        # Use transcribed text if available, otherwise use typed text
        final_scheme_query = st.session_state.get('transcribed_schemes_query', scheme_query)
        
        if not final_scheme_query.strip():
            st.error(f"{t['error_prefix']} {t['no_scheme_query_error']}")
        else:
            with st.spinner(t["processing_schemes"]):
                try:
                    response = asyncio.run(run_government_schemes(
                        scheme_query=final_scheme_query, 
                        language=st.session_state.selected_language
                    ))
                    
                    # Display text response
                    st.markdown(f"""<div class="response-card"><h3>{t['schemes_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    
                    # Generate audio response
                    with st.spinner("🔊 Generating audio response..."):
                        audio_response = text_to_speech(response, st.session_state.selected_language)
                        if audio_response:
                            st.audio(audio_response, format='audio/wav')
                    
                    st.session_state.consultation_history.append({
                        "type": "government_schemes", 
                        "question": final_scheme_query, 
                        "response": response, 
                        "language": st.session_state.selected_language
                    })
                    
                    # Clear transcribed text
                    if 'transcribed_schemes_query' in st.session_state:
                        del st.session_state.transcribed_schemes_query
                        
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Weather Forecast Tab ---
with tab5:
    st.markdown(f"<h2 class='section-header'>{t['weather_header']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['weather_subtitle']}</p>", unsafe_allow_html=True)
    
    # Audio input option
    st.markdown("### 🎤 Voice Input (Optional)")
    audio_input_weather = st.audio_input("Record your location", key="audio_weather_query")
    
    with st.form(key="weather_form"):
        location = st.text_input(label=t["location_label"], placeholder=t["location_placeholder"], key="location_input")
        submit_weather_button = st.form_submit_button(label=t["get_weather_button"])

    # Process audio input if provided
    if audio_input_weather and not submit_weather_button:
        with st.spinner("🎤 Converting speech to text..."):
            audio_bytes = audio_input_weather.read()
            transcribed_text = speech_to_text(audio_bytes, mime_type='audio/wav')
            if transcribed_text:
                st.session_state.transcribed_weather_query = transcribed_text
                st.success(f"📝 Transcribed: {transcribed_text}")
                st.info("👆 Click Submit to get weather forecast")

    if submit_weather_button:
        # Use transcribed text if available, otherwise use typed text
        final_location = st.session_state.get('transcribed_weather_query', location)
        
        if not final_location.strip():
            st.error(f"{t['error_prefix']} {t['no_location_error']}")
        else:
            with st.spinner(t["processing_weather"]):
                try:
                    response = asyncio.run(run_weather_forecast(
                        location=final_location, 
                        language=st.session_state.selected_language
                    ))
                    
                    # Display text response
                    st.markdown(f"""<div class="response-card"><h3>{t['weather_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    
                    # Generate audio response
                    with st.spinner("🔊 Generating audio response..."):
                        audio_response = text_to_speech(response, st.session_state.selected_language)
                        if audio_response:
                            st.audio(audio_response, format='audio/wav')
                    
                    st.session_state.consultation_history.append({
                        "type": "weather_forecast", 
                        "question": f"Weather in {final_location}", 
                        "response": response, 
                        "language": st.session_state.selected_language
                    })
                    
                    # Clear transcribed text
                    if 'transcribed_weather_query' in st.session_state:
                        del st.session_state.transcribed_weather_query
                        
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Consultation History ---
st.markdown(f"<h2 class='section-header history-header'>{t['consultation_history_header']}</h2>", unsafe_allow_html=True)
if st.session_state.consultation_history:
    st.info(f"{t['total_consultations_label']}: {len(st.session_state.consultation_history)}")
    
    history_text = "\n\n".join([f"--- Consultation ---\nType: {h['type']}\nLanguage: {h['language']}\nQuestion: {h['question']}\n\nResponse:\n{h['response']}" for h in reversed(st.session_state.consultation_history)])
    
    st.download_button(
        label=f"💾 {t['download_history_button']}",
        data=history_text.encode('utf-8'),
        file_name="AgriBharat_Consultation_History.txt",
        mime="text/plain",
        key="download_report_button"
    )

else:
    st.info(t["no_history_message"])

# Footer
st.markdown(f"""<div class="footer">{t['footer']}</div>""", unsafe_allow_html=True)