import streamlit as st
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools import google_search 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the Language Agent
qa_agent = Agent(
    name="QuestionAnsweringAgent",
    model="gemini-2.5-pro",
    description="A helpful assistant that answers user questions.",
    instruction="You are a helpful and knowledgeable AI assistant. Your goal is to answer the user's question directly and accurately.",
    tools=[google_search]
)

# Asynchronous function to run the agent
async def run_qa_agent(user_question: str):
    """
    This function sets up the required Runner and Session to execute the Q&A agent.
    """
    # Set up the session service
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="qa_app", user_id="user1", session_id="session1"
    )

    # Set up the runner
    runner = Runner(
        agent=qa_agent,
        app_name="qa_app",
        session_service=session_service
    )

    # Prepare the user message
    user_message = types.Content(
        role='user',
        parts=[types.Part(text=user_question)]
    )

    # Execute the agent
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

# Streamlit app layout
st.set_page_config(page_title="Question Answering Agent", layout="centered")

# Add Tailwind CSS via CDN for basic styling
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# App title
st.markdown("""
    <h1 class="text-3xl font-bold text-center mb-6">Question Answering Agent</h1>
""", unsafe_allow_html=True)

# Input form
with st.form(key="question_form"):
    user_question = st.text_input(
        label="Ask a question:",
        placeholder="e.g., What are the steps to plant a papaya tree?"
    )
    submit_button = st.form_submit_button(label="Get Answer")

# Handle form submission
if submit_button and user_question:
    with st.spinner("Processing your question..."):
        # Run the async function within Streamlit
        try:
            response = asyncio.run(run_qa_agent(user_question))
            st.markdown(f"""
                <div class="mt-4 p-4 bg-gray-100 rounded-lg">
                    <h2 class="text-xl font-semibold">Answer:</h2>
                    <p>{response}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("""
    <p class="text-center text-gray-500 mt-6">
        Powered by Google ADK and Streamlit
    </p>
""", unsafe_allow_html=True)