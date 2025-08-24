import streamlit as st
import os
import tempfile
import requests
from pathlib import Path
from pypdf import PdfReader
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
from together import Together
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- App Configuration ---
st.set_page_config(page_title="RAG App", layout="wide")
st.title("📄🤖 Chat with Your Documents and Urls")
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button {
        background-color: #4CAF50; color: white; border-radius: 12px;
        padding: 10px 24px; border: none; cursor: pointer; font-size: 16px;
    }
    .stTextInput>div>div>input { border-radius: 12px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Configuration")
    # Load API key from .env file or let the user input it
    api_key_from_env = os.getenv("TOGETHER_API_KEY")
    together_api_key = st.text_input(
        "Together AI API Key", 
        type="password", 
        placeholder="Enter your key here or set it in .env",
        value=api_key_from_env
    )

    st.header("📚 Add Your Knowledge")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    url_input = st.text_area("Enter URLs (one per line)", placeholder="https://example.com\nhttps://another-example.com")
    process_button = st.button("Process Documents & URLs")

    st.markdown("---")
    st.header("About")
    st.info("This RAG app, offering more transparent control over the document processing and retrieval pipeline.")

# --- Core Logic ---

# Define the persistent directory for ChromaDB
CHROMA_PERSIST_DIR = "chroma_db_persistent"
COLLECTION_NAME = "documents_collection"

# Initialize the embedding model
@st.cache_resource
def get_embedding_model():
    """Loads the sentence-transformer model."""
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = get_embedding_model()

# Initialize ChromaDB client and collection
@st.cache_resource
def get_chroma_collection():
    """Initializes a persistent ChromaDB client and gets/creates a collection."""
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection

collection = get_chroma_collection()

def simple_text_splitter(text, chunk_size=1000, chunk_overlap=200):
    """A simple text splitter function."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def process_data(files, urls):
    """Loads, splits, and embeds documents and URLs."""
    all_text = ""
    sources = []
    with st.spinner('Processing your sources... This may take a moment.'):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Process PDFs
            for file in files:
                file_path = Path(temp_dir) / file.name
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                
                reader = PdfReader(str(file_path))
                pdf_text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
                all_text += pdf_text + "\n"
                sources.append(file.name)

        # Process URLs
        url_list = [url.strip() for url in urls.split("\n") if url.strip()]
        for url in url_list:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                url_text = soup.get_text(separator='\n', strip=True)
                all_text += url_text + "\n"
                sources.append(url)
            except Exception as e:
                st.error(f"Failed to fetch URL {url}: {e}")

        if all_text:
            chunks = simple_text_splitter(all_text)
            if chunks:
                ids = [str(uuid.uuid4()) for _ in chunks]
                embeddings = embedding_model.encode(chunks, show_progress_bar=True).tolist()
                metadatas = [{"source": ", ".join(sources)} for _ in chunks]
                
                collection.add(
                    embeddings=embeddings,
                    documents=chunks,
                    metadatas=metadatas,
                    ids=ids
                )
                st.success(f"Successfully processed and embedded content from {len(sources)} source(s).")
            else:
                st.warning("Could not extract any text to process.")
        else:
            st.warning("No new documents or URLs to process.")

if process_button:
    if not uploaded_files and not url_input:
        st.error("Please upload at least one PDF or enter a URL.")
    else:
        process_data(uploaded_files, url_input)

# --- Chat Interface ---
st.header("💬 Ask Your Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not together_api_key:
        st.error("Please enter your Together AI API key in the sidebar or set it in your .env file.")
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    # 1. Embed the user's query
                    query_embedding = embedding_model.encode(prompt).tolist()

                    # 2. Query ChromaDB for relevant context
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=3 # Retrieve top 3 most relevant chunks
                    )
                    
                    retrieved_docs = results.get('documents', [[]])[0]
                    context = "\n\n---\n\n".join(retrieved_docs)
                    
                    # 3. Construct the prompt for the LLM
                    formatted_prompt = f"""
                    Use the following context to answer the question at the end. If you don't know the answer from the context, just say that you don't know.

                    Context:
                    {context}

                    Question:
                    {prompt}

                    Answer in human-readable format.
                    """

                    # 4. Call the Together AI API using the official library
                    client = Together(api_key=together_api_key)
                    
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3-8b-chat-hf",
                        messages=[{"role": "user", "content": formatted_prompt}],
                        temperature=0.7,
                        max_tokens=512
                    )
                    
                    full_response = response.choices[0].message.content

                    # Display the source documents
                    with st.expander("📚 Source Context"):
                        st.write(context if context else "No relevant context found in the database.")

                except Exception as e:
                    full_response = f"An error occurred: {e}"

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
