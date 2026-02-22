import streamlit as st
import sys
sys.path.append('./Chatbot')
sys.path.append('./RAGAgent')
pages = {
    "Resources": [
        st.Page("Chatbot/chatbot.py", title="ChatBot"),
        st.Page("RAGAgent/agent.py", title="RAGAgent")
    ],
}

pg = st.navigation(pages, position="top")
pg.run()