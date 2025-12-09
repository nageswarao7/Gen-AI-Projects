
import asyncio
import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Language Instruction Mapping ---
language_instructions = {
    "English": "Respond in English.",
    "Hindi": "हिंदी में जवाब दें।",
    "Telugu": "సమాధానాన్ని తెలుగులో ఇవ్వండి.",
    "Kannada": "ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ.",
    "Malayalam": "മലയാളത്തിൽ മറുപടി നൽകുക.",
    "Tamil": "தமிழில் பதிலளிக்கவும்."
}

# --- Define Agents ---
# Question Answering Agent (for crop queries)
qa_agent = LlmAgent(
    name="QuestionAnsweringAgent",
    model="gemini-2.5-flash",
    description="A helpful assistant that answers crop-related questions for Indian farmers in the specified language.",
    instruction="You are a helpful and knowledgeable AI assistant for Indian farmers. Answer the user's crop-related question directly and accurately in the language specified in the query, focusing on practical advice for small-scale farming in India.",
    tools=[google_search]
)

# Vision Agent (for image analysis)
vision_agent = LlmAgent(
    name="VisionAgent",
    model="gemini-2.5-flash",
    description="Analyzes plant images and identifies diseases.",
    instruction="You are an expert in analyzing plant images. Identify potential diseases in the provided plant image and save the analysis to the state under 'disease_analysis'. Include disease name, symptoms, and confidence level if possible.",
    output_key="disease_analysis",
    tools=[google_search]
)

# Treatment Agent (for pesticide and precaution recommendations)
treatment_agent = LlmAgent(
    name="TreatmentAgent",
    model="gemini-2.5-flash",
    description="Generates pesticide recommendations and precautions based on disease analysis.",
    instruction="You are an expert in plant disease treatment. Using the disease analysis from state['disease_analysis'], provide detailed pesticide recommendations, application methods, and precautions in the language specified in the query. Focus on affordable, locally available remedies for small-scale farmers in India.",
    tools=[google_search]
)

# Language Agent (for generating explanations)
language_agent = LlmAgent(
    name="LanguageAgent",
    model="gemini-2.5-flash",
    description="Generates a detailed explanation based on disease and treatment analysis in the specified language.",
    instruction="You are an expert in generating detailed explanations from plant disease analyses. Use the analysis from state['disease_analysis'] and state['treatment_recommendations'] to create a comprehensive report on plant leaf diseases, including identified diseases, symptoms, treatments, and precautions, in the language specified in the query.",
    tools=[google_search]
)

# Image Explanation Agent (combines vision, treatment, and language agents)
image_explanation_agent = SequentialAgent(
    name="ImageExplanationAgent",
    sub_agents=[vision_agent, treatment_agent, language_agent]
)

# Market Analysis Agent (for crop market trends)
market_analysis_agent = LlmAgent(
    name="MarketAnalysisAgent",
    model="gemini-2.5-flash",
    description="Analyzes market trends for a specified crop in India.",
    instruction="You are an expert in agricultural market analysis. Use the Google Search tool to fetch recent market trends (e.g., price trends, demand, supply) for the specified crop in India, and summarize them in a concise report in the language specified in the query. Prioritize data from local mandis or reliable agricultural sources like Agmarknet or e-NAM.",
    tools=[google_search]
)

# Government Schemes Agent
government_schemes_agent = LlmAgent(
    name="GovernmentSchemesAgent",
    model="gemini-2.5-flash",
    description="Fetches and summarizes government agricultural schemes for farmers in India.",
    instruction="You are an expert in Indian agricultural government schemes. Use the Google Search tool to fetch details about the specified scheme or need (e.g., subsidies for drip irrigation) from official Indian government websites (e.g., PMKSY, e-NAM). Summarize the scheme in simple terms, list eligibility requirements, and provide links to application portals in the language specified in the query.",
    tools=[google_search]
)

# Weather Agent
weather_agent = LlmAgent(
    name="WeatherAgent",
    model="gemini-2.5-flash",
    description="Fetches weather forecast for a specified location in India.",
    instruction="You are a helpful weather assistant for farmers. Use the Google Search tool to fetch the current weather and a 3-day forecast for the specified location in India. Include temperature, rainfall probability, and humidity. Provide the information in a clear, concise format in the language specified in the query.",
    tools=[google_search]
)

# --- Asynchronous Function to Run Text Question Agent ---
async def run_qa_agent(user_question: str, language: str):
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="qa_app", user_id="user1", session_id="session1")
    runner = Runner(
        agent=qa_agent,
        app_name="qa_app",
        session_service=session_service
    )
    full_query = f"{user_question}\n{language_instructions[language]}"
    user_message = types.Content(
        role='user',
        parts=[types.Part(text=full_query)]
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        return final_response if final_response else "The agent did not provide a response."
    except Exception as e:
        return f"An error occurred during agent execution: {e}"

# --- Asynchronous Function to Run Image Explanation Agent ---
async def run_comprehensive_disease_analysis(image_data: bytes, user_question: str, language: str):
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="image_app", user_id="user1", session_id="session1")
    runner = Runner(
        agent=image_explanation_agent,
        app_name="image_app",
        session_service=session_service
    )
    full_query = f"{user_question}\n{language_instructions[language]}"
    user_message = types.Content(
        role='user',
        parts=[
            types.Part(text=full_query),
            types.Part.from_bytes(data=image_data, mime_type='image/jpeg')
        ]
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        return final_response if final_response else "The agent did not provide a response."
    except Exception as e:
        return f"An error occurred during agent execution: {e}"

# --- Asynchronous Function to Run Market Analysis Agent ---
async def run_market_analysis(crop_name: str, language: str):
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="market_app", user_id="user1", session_id="session1")
    runner = Runner(
        agent=market_analysis_agent,
        app_name="market_app",
        session_service=session_service
    )
    full_query = f"Provide recent market trends for {crop_name} in India, including price trends, demand, and supply information.\n{language_instructions[language]}"
    user_message = types.Content(
        role='user',
        parts=[types.Part(text=full_query)]
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        return final_response if final_response else "No market data available for the specified crop."
    except Exception as e:
        return f"An error occurred during market analysis: {e}"

# --- Asynchronous Function to Run Government Schemes Agent ---
async def run_government_schemes(scheme_query: str, language: str):
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="schemes_app", user_id="user1", session_id="session1")
    runner = Runner(
        agent=government_schemes_agent,
        app_name="schemes_app",
        session_service=session_service
    )
    full_query = f"Fetch details about {scheme_query} from official Indian government agricultural websites. Summarize in simple terms, list eligibility requirements, and provide links to application portals.\n{language_instructions[language]}"
    user_message = types.Content(
        role='user',
        parts=[types.Part(text=full_query)]
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        return final_response if final_response else "No scheme data available for the specified query."
    except Exception as e:
        return f"An error occurred during scheme query: {e}"

# --- Asynchronous Function to Run Weather Forecast Agent ---
async def run_weather_forecast(location: str, language: str):
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="weather_app", user_id="user1", session_id="session1")
    runner = Runner(
        agent=weather_agent,
        app_name="weather_app",
        session_service=session_service
    )
    full_query = f"Fetch the current weather and 3-day forecast for {location}, India.\n{language_instructions[language]}"
    user_message = types.Content(
        role='user',
        parts=[types.Part(text=full_query)]
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        return final_response if final_response else "No weather data available for the specified location."
    except Exception as e:
        return f"An error occurred during weather forecast: {e}"

# Placeholder for backward compatibility
async def run_image_explanation(image_data: bytes, user_question: str, language: str):
    return await run_comprehensive_disease_analysis(image_data, user_question, language)
