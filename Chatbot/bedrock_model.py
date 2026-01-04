import boto3
import json
import streamlit as st
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_classic.memory import ConversationBufferMemory
from app_feature import typing_css, typing_indicator, autoscroll


def bedrock_model_logic(model_id: str, region: str, user_input: str, max_tokens: float, temperature: float):

    # Apply typing CSS
    typing_css()

    ## Define bedrock client
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1"
    )

    ## Configuration Memory
    chat_history = InMemoryChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True,
        ai_prefix="\n\nAssistant",
        human_prefix="\n\nHuman"
    )

    ## Define the prompt template
    messages = ChatPromptTemplate.from_messages(
        [
            ("system", "Hey Human!! I am Alps. Welcome to my place 😊"),
            ("human", "{user_input}"),
        ]
    )
    ## Connect to Bedrock Model
    llm = ChatBedrockConverse(
        client=bedrock_client,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages with regenerate option for assistant messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                col1, col2 = st.columns([9, 1])
                with col1:
                    st.markdown(message["content"])
                with col2:
                    if st.button("⧉", key=f"copy_user_{i}", help="Copy message"):
                        st.write(f'<script>navigator.clipboard.writeText(`{message["content"]}`);</script>', unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
            if message["role"] == "assistant":
                col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 5])
                
                # Get current feedback state
                current_feedback = st.session_state.get(f"feedback_{i}", None)
                
                with col1:
                    like_style = "✅👍" if current_feedback == "liked" else "👍"
                    if st.button(like_style, key=f"like_{i}", help="Good"):
                        st.session_state[f"feedback_{i}"] = "liked"
                        st.rerun()
                with col2:
                    dislike_style = "✅👎" if current_feedback == "disliked" else "👎"
                    if st.button(dislike_style, key=f"dislike_{i}", help="Poor"):
                        st.session_state[f"feedback_{i}"] = "disliked"
                        st.rerun()
                with col3:
                    love_style = "✅❤️" if current_feedback == "loved" else "❤️"
                    if st.button(love_style, key=f"love_{i}", help="Love"):
                        st.session_state[f"feedback_{i}"] = "loved"
                        st.rerun()
                with col4:
                    smile_style = "✅😊" if current_feedback == "smiled" else "😊"
                    if st.button(smile_style, key=f"smile_{i}", help="Nice"):
                        st.session_state[f"feedback_{i}"] = "smiled"
                        st.rerun()
                with col5:
                    if st.button("🔄", key=f"regenerate_{i}", help="Regenerate"):
                        # Find the corresponding user message
                        if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                            user_prompt = st.session_state.messages[i-1]["content"]
                            # Show typing indicator while regenerating
                            typing_placeholder = st.empty()
                            with typing_placeholder:
                                typing_indicator()
                            # Generate new response
                            output_parser = StrOutputParser()
                            chain = messages|llm|output_parser
                            new_response = chain.invoke({"user_input": user_prompt})
                            # Clear typing indicator
                            typing_placeholder.empty()
                            # Update the message
                            st.session_state.messages[i]["content"] = new_response
                            autoscroll()  # Auto-scroll after regeneration
                            st.rerun()

    if user_input:
        with st.chat_message("user"):
            col1, col2 = st.columns([9, 1])
            with col1:
                st.markdown(user_input)
            with col2:
                if st.button("⧉", key="copy_user_new", help="Copy"):
                    st.write(f'<script>navigator.clipboard.writeText(`{user_input}`);</script>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing indicator while generating response
        typing_placeholder = st.empty()
        with typing_placeholder:
            typing_indicator()
        
        output_parser = StrOutputParser()
        chain = messages|llm|output_parser
        response = chain.invoke({"user_input": user_input})
        
        # Clear typing indicator
        typing_placeholder.empty()
        with st.chat_message("assistant"):
            st.markdown(response)
            autoscroll()  # Auto-scroll after new message
            # Add feedback emojis for new response
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 5])
            
            # Get current feedback state for new message
            new_msg_index = len(st.session_state.messages)
            current_feedback = st.session_state.get(f"feedback_{new_msg_index}", None)
            
            with col1:
                like_style = "✅👍" if current_feedback == "liked" else "👍"
                if st.button(like_style, key="like_new", help="Good response"):
                    st.session_state[f"feedback_{new_msg_index}"] = "liked"
                    st.rerun()
            with col2:
                dislike_style = "✅👎" if current_feedback == "disliked" else "👎"
                if st.button(dislike_style, key="dislike_new", help="Poor response"):
                    st.session_state[f"feedback_{new_msg_index}"] = "disliked"
                    st.rerun()
            with col3:
                love_style = "✅❤️" if current_feedback == "loved" else "❤️"
                if st.button(love_style, key="love_new", help="Love this response"):
                    st.session_state[f"feedback_{new_msg_index}"] = "loved"
                    st.rerun()
            with col4:
                smile_style = "✅😊" if current_feedback == "smiled" else "😊"
                if st.button(smile_style, key="smile_new", help="Nice response"):
                    st.session_state[f"feedback_{new_msg_index}"] = "smiled"
                    st.rerun()
            with col5:
                if st.button("🔄", key="regenerate_new", help="Regenerate response"):
                    # Show typing indicator while regenerating
                    typing_placeholder = st.empty()
                    with typing_placeholder:
                        typing_indicator()
                    new_response = chain.invoke({"user_input": user_input})
                    # Clear typing indicator
                    typing_placeholder.empty()
                    st.session_state.messages.append({"role": "assistant", "content": new_response})
                    autoscroll()  # Auto-scroll after regeneration
                    st.rerun()
        st.session_state.messages.append({"role": "assistant", "content": response})