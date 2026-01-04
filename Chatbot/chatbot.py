import boto3
import streamlit as st
from bedrock_model import bedrock_model_logic
from app_feature import apply_sidebar


## Set page configuration
st.set_page_config(page_title="Chatbot", page_icon="img.png", layout="wide")

def app():

    ## Sidebar Settings:
    apply_sidebar()

    ## Title
    st.title(":rainbow[🦜Langchain ChatBot🦜]")

    ## List of models
    model_list = [
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "cohere.command-r-plus-v1:0",
        "cohere.command-r-v1:0"
    ]
    ## Type User Prompt
    user_input = st.chat_input("Ask something")

    ## Define Streamlit Properties
    with st.sidebar:
        st.title('Settings')
        model_id = st.selectbox("### 📈 Select Model", model_list)
        temperature = st.slider("### 🔥 Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Higher = more creative output | Lower = more factual")
        max_tokens = st.slider("### 🧩 Max Tokens", min_value=100, max_value=2048, value=1024, step=100)
        
        if st.button("New Message", type="primary"):
            st.session_state.messages = []
            st.rerun()

        st.divider()
        
        # Display user prompts
        st.title("Chat History")
        if "messages" in st.session_state:
            user_prompts = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
            if user_prompts:
                for i, prompt in enumerate(user_prompts, 1):
                    # with st.expander(f"Prompt {i}"):
                        st.write(prompt)
            else:
                st.write("No prompts yet")
        else:
            st.write("No prompts yet")
    region = "us-east-1"
    bedrock_model_logic(model_id, region, user_input, max_tokens, temperature)

app()