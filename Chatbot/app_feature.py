import streamlit as st

def typing_indicator():
    return st.markdown("""
    <div class="typing">
        <span>🤖 Bot is typing</span>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    """, unsafe_allow_html=True)

def autoscroll():
    st.markdown("""
    <script>
    var chatBox = window.parent.document.querySelector('.main');
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
    </script>
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
    
    /* Remove red background from buttons with stronger selectors */
    div[data-testid="column"] .stButton > button,
    .stButton > button,
    button[kind="secondary"] {
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: inherit !important;
        box-shadow: none !important;
    }
    
    div[data-testid="column"] .stButton > button:hover,
    .stButton > button:hover,
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    div[data-testid="column"] .stButton > button:focus,
    .stButton > button:focus,
    button[kind="secondary"]:focus {
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_sidebar():
    st.markdown("""
    <style>

    /* Sidebar container */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141414, #1d1d1d);
        padding: 2rem 1.2rem;
        border-right: 1px solid #333;
        animation: fadeIn 0.8s ease-out;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateX(-20px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    /* Section headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #fff !important;
        letter-spacing: .3px;
        animation: slideIn 0.6s ease-in;
    }

    @keyframes slideIn {
        0% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Slider animation + glow */
    .stSlider input:focus + div .thumb {
        box-shadow: 0 0 12px #ff3e3e;
        transition: 0.3s;
    }

    /* Hover animation on dropdown */
    .stSelectbox > div > div:hover {
        transform: scale(1.02);
        transition: 0.25s ease-in-out;
    }

    /* Animated button style */
    .stButton button {
        background: #e50914;
        color: white;
        padding: .6rem 1.2rem;
        border-radius: 8px;
        border: none;
        transition: .25s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        background: #ff1b2d;
        box-shadow: 0 3px 10px rgba(255,0,0,0.4);
    }

    </style>
    """, unsafe_allow_html=True)