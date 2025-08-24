import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import LangChain components
from langchain_together import ChatTogether
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# --- AGENT CONFIGURATION ---

# 1. Initialize the LLM
llm = ChatTogether(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
)

# 2. Define the Tools the Agent Can Use

search = GoogleSerperAPIWrapper()

# MODIFIED: Now uses "w" (write mode) to overwrite the file
def write_note_to_file(note_content: str) -> str:
    """Saves a note to 'notes.txt', overwriting previous content."""
    try:
        # --- FIX ---
        # Clean the input string to remove potential agent artifacts like "Observ".
        # This splits the string by the word "Observ" and keeps only the text before it.
        cleaned_content = note_content.split("Observ")[0].strip()
        # --- END FIX ---
        # Using "w" to write/overwrite the file instead of "a" to append
        with open("notes.txt", "w") as f:
            f.write(cleaned_content + "\n")
        return "Note saved successfully"
    except Exception as e:
        return f"Failed to save note. Error: {e}"

def summarize_pdf(dummy_input: str) -> str:
    """Summarizes the content of the uploaded PDF file."""
    if "uploaded_pdf_path" not in st.session_state or not st.session_state.uploaded_pdf_path:
        return "No PDF uploaded. Please upload a PDF first."
    
    try:
        loader = PyPDFLoader(st.session_state.uploaded_pdf_path)
        docs = loader.load()
        chain = load_summarize_chain(llm, chain_type="stuff")
        result = chain.invoke(docs)
        summary = result.get("output_text", "Could not extract summary.")
        # Clean up the temporary file after summarization
        os.remove(st.session_state.uploaded_pdf_path)
        del st.session_state.uploaded_pdf_path
        return summary
    except Exception as e:
        return f"Failed to summarize PDF. Error: {e}"

# Create a list of tools
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for answering questions about current events, weather, or facts.",
    ),
    # MODIFIED: Description is now stricter
    Tool(
        name="WriteNote",
        func=write_note_to_file,
        description="Strictly use this tool ONLY when the user's command explicitly includes 'save note'. This saves text to a file, overwriting any previous note. The input should be the content of the note that follows 'save note:'",
    ),
    Tool(
        name="SummarizePDF",
        func=summarize_pdf,
        description="Useful for summarizing the uploaded PDF when the user asks.",
    ),
]

custom_react_template = """
You are a helpful task automation agent. You can respond directly to general questions, greetings, and conversations, OR use tools when needed.

You have access to these tools:
{tools}

Tool names available: {tool_names}

IMPORTANT: Only use tools when absolutely necessary:
- Use Search tool for current events, weather, or facts you don't know
- Use WriteNote tool ONLY when user says "save note:" 
- Use SummarizePDF tool when user asks to summarize an uploaded PDF
- For greetings, general chat, or questions you can answer directly, respond WITHOUT using any tools

When you need to use a tool, follow this format:
Question: {input}
Thought: I need to use a tool for this request
Action: [one of {tool_names}]
Action Input: [input for the tool]
Observation: [tool result]
Final Answer: [your response based on the tool result for the note saved should strictly give the same output as from the tool.]  

When you don't need tools, respond directly:
Question: {input}
Final Answer: [your direct response]

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""


# Create the prompt template
prompt_template = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template=custom_react_template
)

# 4. Create the Agent with custom prompt
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- STREAMLIT UI ---

st.set_page_config(page_title="Task Automation Agent", page_icon="🤖", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .stDownloadButton > button {
        background-color: #008CBA;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Task Automation Agent")
st.caption("Your personal assistant powered by Llama-3 and LangChain. Chat with me to search info, save notes, or summarize PDFs!")

# Sidebar for PDF Uploader and Instructions
st.sidebar.title("📤 Upload PDF")
uploaded_pdf = st.sidebar.file_uploader("Choose a PDF file for summarization", type="pdf")
if uploaded_pdf is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_pdf.getbuffer())
        st.session_state.uploaded_pdf_path = tmp_file.name
    st.sidebar.success("PDF uploaded successfully! Ask me to summarize it.")

st.sidebar.markdown("### 📋 Instructions")
st.sidebar.markdown("- **Search**: Ask about current events, weather, or facts.")
st.sidebar.markdown("- **Save Note**: Use 'save note: your note here' to save (overwrites previous).")
st.sidebar.markdown("- **Summarize PDF**: Upload a PDF and ask to summarize it.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input("Enter your command (e.g., 'save note: call mom' or 'summarize the PDF')")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.spinner("Thinking..."):
        response = agent_executor.invoke({"input": user_query})

    output = response["output"]
    st.session_state.messages.append({"role": "assistant", "content": output})
    with st.chat_message("assistant"):
        st.markdown(output)

    if "Note saved successfully" in output:
        if os.path.exists("notes.txt"):
            with open("notes.txt", "rb") as f:
                st.download_button(
                    label="📥 Download Note",
                    data=f,
                    file_name="notes.txt",
                    mime="text/plain",
                    key="download_note"  # Unique key to avoid conflicts
                )