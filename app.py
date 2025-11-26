import streamlit as st
import requests
from datetime import datetime
import json

# CONFIGURATION

API_URL = "https://trophoplasmic-removed-cecily.ngrok-free.dev"

st.set_page_config(
    page_title="Smart Diet Assistant",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .title {
        font-size: 2rem;
        text-align: center;
        color: #666;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: white;
        border: 2px solid #e0e0e0;
        color: #333;
        margin-right: 2rem;
    }
    .message-content {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
    }
    .user-message .message-content {
        color: white;
    }
    .items-list {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .items-list h4 {
        color: #2E7D32;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    .items-list ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    .items-list li {
        color: #333;
        margin: 0.3rem 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .mode-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .mode-document {
        background-color: #E3F2FD;
        color: #1565C0;
    }
    .mode-general {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    .mode-default {
        background-color: #FFF9C4;
        color: #F57F17;
    }
    .confidence-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        margin-left: 0.5rem;
    }
    .confidence-high {
        background-color: #C8E6C9;
        color: #1B5E20;
    }
    .confidence-medium {
        background-color: #FFF9C4;
        color: #F57F17;
    }
    .confidence-low {
        background-color: #FFCDD2;
        color: #B71C1C;
    }
    .source-info {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# SESSION STATE INITIALIZATION

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_health" not in st.session_state:
    st.session_state.api_health = None

# HELPER FUNCTIONS

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except Exception as e:
        return False, str(e)

def ask_question(query):
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"query": query},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def upload_diet_plan(uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(
            f"{API_URL}/upload-diet-plan",
            files=files,
            timeout=60
        )
        if response.status_code == 200:
            return True, response.json()
        return False, f"Upload failed: {response.status_code}"
    except Exception as e:
        return False, str(e)

def format_assistant_message(response_data):
    if isinstance(response_data, str):
        return response_data
    
    # Extract data - now answer is already clean!
    answer = response_data.get("answer", "I couldn't find an answer.")
    mode = response_data.get("mode", "")
    items = response_data.get("items", [])
    source = response_data.get("source", "")
    confidence = response_data.get("confidence", "")
    key_points = response_data.get("key_points", [])
    notes = response_data.get("notes", "")
    
    # Start building HTML
    html_parts = []
    
    # Add mode badge
    mode_emoji = {
        "DOCUMENT": "📋",
        "GENERAL": "💡",
        "DEFAULT": "🔍"
    }
    mode_class = f"mode-{mode.lower()}" if mode else "mode-default"
    html_parts.append(f'<span class="mode-badge {mode_class}">{mode_emoji.get(mode, "❓")} {mode or "DEFAULT"}</span>')
    
    # Add confidence badge if available
    if confidence:
        conf_class = f"confidence-{confidence.lower()}"
        conf_emoji = {"high": "✅", "medium": "⚠️", "low": "❓"}
        html_parts.append(f'<span class="confidence-badge {conf_class}">{conf_emoji.get(confidence.lower(), "")} {confidence.upper()}</span>')
    
    html_parts.append("<br><br>")
    
    # Add the clean answer (no JSON!)
    html_parts.append(f'<div class="message-content">{answer}</div>')
    
    # Add key points if available (for general knowledge)
    if key_points:
        html_parts.append('<div class="items-list">')
        html_parts.append('<h4>Key Points:</h4>')
        html_parts.append('<ul>')
        for point in key_points:
            html_parts.append(f'<li>{point}</li>')
        html_parts.append('</ul>')
        html_parts.append('</div>')
    
    # Add items list if available (for diet plan questions)
    if items:
        html_parts.append('<div class="items-list">')
        html_parts.append('<h4>Food Items:</h4>')
        html_parts.append('<ul>')
        for item in items:
            html_parts.append(f'<li>{item}</li>')
        html_parts.append('</ul>')
        html_parts.append('</div>')
    
    # Add notes if available
    if notes:
        html_parts.append(f'<div class="source-info">📝 Note: {notes}</div>')
    
    # Add source information
    if source:
        html_parts.append(f'<div class="source-info">Source: {source}</div>')
    
    return "".join(html_parts)

# SIDEBAR

with st.sidebar:
    st.markdown("### Settings")
    
    # API Configuration
    st.markdown("#### API Configuration")
    api_url_input = st.text_input(
        "API URL",
        value=API_URL,
        help="Enter your ngrok URL from Kaggle"
    )
    
    if api_url_input != API_URL:
        API_URL = api_url_input
    
    # Check API Health
    if st.button("Check API Health", use_container_width=True):
        with st.spinner("Checking..."):
            is_healthy, health_data = check_api_health()
            st.session_state.api_health = (is_healthy, health_data)
    
    # Display health status
    if st.session_state.api_health:
        is_healthy, health_data = st.session_state.api_health
        if is_healthy:
            st.success("✅ API is online")
        else:
            st.error(f"❌ API is offline")
            st.code(health_data)
    
    st.divider()
    
    # Upload new diet plan
    st.markdown("#### Upload Diet Plan")
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        help="Upload a new diet plan to update the knowledge base"
    )
    
    if uploaded_file:
        if st.button("Upload", use_container_width=True):
            with st.spinner("Uploading..."):
                success, result = upload_diet_plan(uploaded_file)
                if success:
                    st.success(f"✅ Uploaded! {result.get('chunks', 0)} chunks created")
                else:
                    st.error(f"❌ {result}")
    
    st.divider()
    
    # Clear chat
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Example questions
    st.markdown("#### Example Questions")
    example_questions = [
        "What should I eat for day 1 breakfast?",
        "Can I replace rice with quinoa?",
        "What are the benefits of blueberries?",
        "How many calories in a turkey burger?"
    ]
    
    for question in example_questions:
        if st.button(f"{question}", use_container_width=True, key=question):
            st.session_state.messages.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now()
            })
            
            with st.spinner("🤔 Thinking..."):
                response = ask_question(question)
                
                if "error" in response:
                    answer = f"❌ Error: {response['error']}"
                else:
                    answer = response
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.now()
                })
            
            st.rerun()

# MAIN CONTENT

# Header
st.markdown('<div class="main-header">🥗 Smart Diet Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered nutrition guidance</div>', unsafe_allow_html=True)

if st.session_state.messages==[]:
    st.markdown('<div class="title">Ask anything about your diet plan or nutrition</div>', unsafe_allow_html=True)


# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong><br><br>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Format assistant message
        formatted_content = format_assistant_message(content)
        
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant</strong><br><br>
            {formatted_content}
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask anything about your diet plan or nutrition...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Get response
    with st.spinner("🤔 Thinking..."):
        response = ask_question(user_input)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
    
    st.rerun()

