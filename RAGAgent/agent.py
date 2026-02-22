import boto3
import streamlit as st
from typing import List
import time

from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import S3DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_core.documents import Document

from opensearchpy import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# ============================================================
# CONFIGURATION
# ============================================================

AWS_REGION = "us-east-1"

S3_BUCKET = "rag-agent-knowledge-base-98770"
OPENSEARCH_HOST = "https://search-mydemanricsearchdomain-4eyf4nluuhgpvd6unuyfgvnnyq.us-east-1.es.amazonaws.com"
OPENSEARCH_INDEX = "rag-index"

VECTOR_FIELD = "vector_field"
ENGINE = "faiss"

EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"

LLM_MODEL_LIST = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "cohere.command-r-plus-v1:0",
    "cohere.command-r-v1:0"
]

CATEGORIES = (
    "Technical",
    "Healthcare",
    "Agriculture",
    "Travelling",
    "Gadgets",
    "Music",
    "Cooking",
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def typing_indicator():
    return st.markdown("""
    <div class="typing">
        <span>🤖 Bot is typing</span>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    """, unsafe_allow_html=True)

def typing_css():
    st.markdown("""
    <style>
    .typing {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #ccc;
        font-size: 15px;
        font-style: italic;
        opacity: 0.9;
        margin: 8px 0;
    }
    .dot {
        height: 6px;
        width: 6px;
        background: #ccc;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }
    .dot:nth-child(2) { animation-delay: .2s; }
    .dot:nth-child(3) { animation-delay: .4s; }
    @keyframes blink {
        0% { opacity: .2; }
        20% { opacity: 1; }
        100% { opacity: .2; }
    }
    </style>
    """, unsafe_allow_html=True)

def categorize_prompt(user_input: str, llm) -> str:
    """Use LLM to categorize user prompt"""
    prompt = f"""Classify this question into ONE category from: {', '.join(CATEGORIES)}
Question: {user_input}
Return ONLY the category name."""
    response = llm.invoke(prompt)
    category = response.content.strip()
    return category if category in CATEGORIES else CATEGORIES[0]

# ============================================================
# STREAMLIT PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🦜 RAG Agent",
    page_icon="🦜",
    layout="wide"
)

st.title("🦜 RAG Agent (Bedrock + S3 + Langchain + OpenSearch)")

# Apply typing CSS
typing_css()

# ============================================================
# AWS CLIENTS
# ============================================================

s3 = boto3.client("s3", region_name=AWS_REGION)
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)

session = boto3.Session()
credentials = session.get_credentials()

aws_auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    AWS_REGION,
    "es",
    session_token=credentials.token,
)

# ============================================================
# SIDEBAR – CONFIGURATION
# ============================================================

with st.sidebar:
    st.header("⚙️ Configuration")

    if st.button("🆕 New Chat", type="primary", use_container_width=True):
        st.session_state.agent_messages = []
        st.rerun()

    model_id = st.selectbox("📈 Select LLM", LLM_MODEL_LIST)
    temperature = st.slider("🔥 Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("🧩 Max Tokens", 256, 2048, 1024, 128)
    upload_category = st.selectbox("Select Category for Upload", CATEGORIES, key="upload_cat")
    uploaded_files = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("⬆️ Upload to S3", type="primary"):
        if uploaded_files:
            #upload_category = st.selectbox("Select Category for Upload", CATEGORIES, key="upload_cat")
            for file in uploaded_files:
                s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=f"{upload_category}/{file.name.replace(' ', '_')}",
                    Body=file.getvalue()
                )
            st.success("✅ Files uploaded to S3")
        else:
            st.warning("Please upload at least one PDF")

# ============================================================
# PROMPT TEMPLATE (RAG)
# ============================================================

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Answer using the provided context and chat history when available. "
            "If the answer is not in the context, use your own knowledge to provide a helpful response."
        ),
        (
            "human",
            "Chat History:\n{chat_history}\n\nContext:\n{context}\n\nQuestion:\n{question}"
        ),
    ]
)

# ============================================================
# LLM
# ============================================================

llm = ChatBedrockConverse(
    client=bedrock_runtime,
    model_id=model_id,
    temperature=temperature,
    max_tokens=max_tokens
)

# ============================================================
# VECTOR STORE (CACHED)
# ============================================================

@st.cache_resource(show_spinner="🔍 Indexing documents...")
def build_vectorstore(selected_category: str) -> OpenSearchVectorSearch:
    loader = S3DirectoryLoader(
        bucket=S3_BUCKET,
        prefix=selected_category
    )
    documents = loader.load()

    if not documents:
        raise ValueError("No documents found in this category")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = splitter.split_documents(documents)

    embeddings = BedrockEmbeddings(
        model_id=EMBEDDING_MODEL_ID,
        region_name=AWS_REGION
    )

    vectorstore = OpenSearchVectorSearch(
        index_name=OPENSEARCH_INDEX,
        embedding_function=embeddings,
        http_auth=aws_auth,
        opensearch_url=OPENSEARCH_HOST,
        engine=ENGINE,
        vector_field=VECTOR_FIELD,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    vectorstore.add_documents(splits)
    return vectorstore

# ============================================================
# CHAT HISTORY
# ============================================================

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

for i, msg in enumerate(st.session_state.agent_messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 6])
            current_feedback = st.session_state.get(f"agent_feedback_{i}", None)
            
            with col1:
                like_style = "✅👍" if current_feedback == "liked" else "👍"
                if st.button(like_style, key=f"agent_like_{i}", help="Good"):
                    st.session_state[f"agent_feedback_{i}"] = "liked"
                    st.rerun()
            with col2:
                dislike_style = "✅👎" if current_feedback == "disliked" else "👎"
                if st.button(dislike_style, key=f"agent_dislike_{i}", help="Poor"):
                    st.session_state[f"agent_feedback_{i}"] = "disliked"
                    st.rerun()
            with col3:
                love_style = "✅❤️" if current_feedback == "loved" else "❤️"
                if st.button(love_style, key=f"agent_love_{i}", help="Love"):
                    st.session_state[f"agent_feedback_{i}"] = "loved"
                    st.rerun()
            with col4:
                if st.button("🔄", key=f"agent_regenerate_{i}", help="Regenerate"):
                    if i > 0 and st.session_state.agent_messages[i-1]["role"] == "user":
                        user_prompt = st.session_state.agent_messages[i-1]["content"]
                        
                        typing_placeholder = st.empty()
                        with typing_placeholder:
                            typing_indicator()
                        
                        category = categorize_prompt(user_prompt, llm)
                        vectorstore = build_vectorstore(category)
                        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                        docs = retriever.invoke(user_prompt)
                        context = "\n\n".join(doc.page_content for doc in docs)
                        chat_history = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.agent_messages[:i-1])
                        prompt = rag_prompt.invoke({"chat_history": chat_history, "context": context, "question": user_prompt})
                        new_response = llm.invoke(prompt)
                        
                        typing_placeholder.empty()
                        st.session_state.agent_messages[i]["content"] = new_response.content
                        st.rerun()

# ============================================================
# USER INPUT → RETRIEVAL → ANSWER
# ============================================================

user_input = st.chat_input("Ask a question from your documents...")

if user_input:
    st.session_state.agent_messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            typing_placeholder = st.empty()
            with typing_placeholder:
                typing_indicator()
            
            # Auto-categorize using LLM
            category = categorize_prompt(user_input, llm)
            
            typing_placeholder.empty()
            st.info(f"📂 Detected Category: **{category}**")
            
            typing_placeholder = st.empty()
            with typing_placeholder:
                typing_indicator()
            
            vectorstore = build_vectorstore(category)
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )

            docs = retriever.invoke(user_input)

            context = "\n\n".join(
                doc.page_content for doc in docs
            )

            # Build chat history
            chat_history = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}" 
                for msg in st.session_state.agent_messages[:-1]
            )

            prompt = rag_prompt.invoke(
                {
                    "chat_history": chat_history,
                    "context": context,
                    "question": user_input
                }
            )

            response = llm.invoke(prompt)
            
            typing_placeholder.empty()
            st.markdown(response.content)

            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 6])
            new_msg_index = len(st.session_state.agent_messages)
            current_feedback = st.session_state.get(f"agent_feedback_{new_msg_index}", None)
            
            with col1:
                like_style = "✅👍" if current_feedback == "liked" else "👍"
                if st.button(like_style, key="agent_like_new", help="Good"):
                    st.session_state[f"agent_feedback_{new_msg_index}"] = "liked"
                    st.rerun()
            with col2:
                dislike_style = "✅👎" if current_feedback == "disliked" else "👎"
                if st.button(dislike_style, key="agent_dislike_new", help="Poor"):
                    st.session_state[f"agent_feedback_{new_msg_index}"] = "disliked"
                    st.rerun()
            with col3:
                love_style = "✅❤️" if current_feedback == "loved" else "❤️"
                if st.button(love_style, key="agent_love_new", help="Love"):
                    st.session_state[f"agent_feedback_{new_msg_index}"] = "loved"
                    st.rerun()
            with col4:
                if st.button("🔄", key="agent_regenerate_new", help="Regenerate"):
                    typing_placeholder = st.empty()
                    with typing_placeholder:
                        typing_indicator()
                    
                    category = categorize_prompt(user_input, llm)
                    vectorstore = build_vectorstore(category)
                    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                    docs = retriever.invoke(user_input)
                    context = "\n\n".join(doc.page_content for doc in docs)
                    chat_history = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.agent_messages[:-1])
                    prompt = rag_prompt.invoke({"chat_history": chat_history, "context": context, "question": user_input})
                    new_response = llm.invoke(prompt)
                    response = new_response
                    
                    typing_placeholder.empty()
                    st.rerun()

            st.session_state.agent_messages.append(
                {"role": "assistant", "content": response.content}
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")