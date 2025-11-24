import streamlit as st
import requests
import datetime
import uuid
import json
import httpx
import asyncio
from utils.pdf_generator import generate_pdf
import os

# Load environment variables or defaults
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="🌍 Global Travel Planner", page_icon="✈️", layout="wide")

# Custom CSS 
st.markdown("""
<style>
    /* Global Settings */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Chat Message Container */
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #444;
    }
    
    /* Force text color for all elements inside chat messages */
    .stChatMessage .stMarkdown, 
    .stChatMessage p, 
    .stChatMessage div, 
    .stChatMessage li, 
    .stChatMessage h1, 
    .stChatMessage h2, 
    .stChatMessage h3, 
    .stChatMessage h4, 
    .stChatMessage h5, 
    .stChatMessage h6 {
        color: #ffffff !important;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
        transform: scale(1.02);
    }
    
    /* PDF Download Button - Better Visibility */
    .stDownloadButton>button {
        background-color: #4b8bff !important;
        color: white !important;
        border: 2px solid #6ba3ff !important;
        font-weight: bold !important;
    }
    .stDownloadButton>button:hover {
        background-color: #6ba3ff !important;
        border-color: #4b8bff !important;
    }
    
    /* Headers */
    h1 {
        color: #ff4b4b !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        color: #4b8bff !important;
    }
    
    /* Links */
    .stMarkdown a {
        color: #4b8bff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Global Travel Planner")
st.markdown("### *Plan your perfect trip with AI - Hotels, Restaurants, Bakeries & More*")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Sidebar for options
with st.sidebar:
    st.header("Settings")
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
    st.info(f"Session ID: {st.session_state.thread_id}")
    
    # Push developer badge to bottom with spacer
    st.markdown("<br>" * 18, unsafe_allow_html=True)
    
    # Developer badge at bottom of sidebar
    st.markdown("""
    <div style="
        background: rgba(38, 39, 48, 0.95);
        padding: 12px 20px;
        border-radius: 25px;
        border: 2px solid #4b8bff;
        text-align: center;
        transition: all 0.3s ease;
    " onmouseover="this.style.background='rgba(75, 139, 255, 0.2)'; this.style.borderColor='#6ba3ff'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 15px rgba(75, 139, 255, 0.3)';" 
       onmouseout="this.style.background='rgba(38, 39, 48, 0.95)'; this.style.borderColor='#4b8bff'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        <p style="margin: 0; color: #ffffff; font-size: 0.9rem; font-weight: 600;">
            Developed by <span style="color: #4b8bff; font-weight: bold;">PRANAV</span> 👨‍💻
        </p>
    </div>
    """, unsafe_allow_html=True)

# Helper for PDF generation (cached to avoid re-generating on every rerun)
@st.cache_data
def get_pdf_data(content):
    return generate_pdf(content, return_bytes=True)

# Chat Input - Moved to top
if prompt := st.chat_input("Ex. Plan a cost-effective trip to Würzburg with recommendations for budget hotels, traditional bakeries, and getting around the city."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Status container for tool updates
        with st.status("🤔 Thinking...", expanded=True) as status:
            try:
                with requests.post(
                    f"{BASE_URL}/chat/stream", 
                    json={"question": prompt, "thread_id": st.session_state.thread_id}, 
                    stream=True
                ) as r:
                    for line in r.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            if decoded_line.startswith("data: "):
                                data_str = decoded_line[6:]
                                if data_str == "[DONE]":
                                    break
                                try:
                                    event_data = json.loads(data_str)
                                    
                                    if isinstance(event_data, dict):
                                        # Handle Tool Calls (from 'agent' node outputting tool_calls)
                                        if 'agent' in event_data:
                                            agent_msgs = event_data['agent'].get('messages', [])
                                            if agent_msgs:
                                                msg = agent_msgs[0]
                                                # Check for tool_calls in the message
                                                if 'tool_calls' in msg and msg['tool_calls']:
                                                    for tool_call in msg['tool_calls']:
                                                        tool_name = tool_call.get('name', 'Tool')
                                                        tool_args = tool_call.get('args', {})
                                                        status.write(f"🛠️ **Using Tool:** `{tool_name}`")
                                                        status.write(f"Input: `{tool_args}`")
                                                
                                                # Check for final content
                                                content = msg.get('content', '')
                                                if content:
                                                    # Remove raw function call tags
                                                    import re
                                                    cleaned_content = re.sub(r'<function=.*?>.*?</function>', '', content, flags=re.DOTALL).strip()
                                                    full_response = cleaned_content if cleaned_content else content
                                                    message_placeholder.markdown(full_response)

                                        # Handle Tool Outputs (from 'tools' node)
                                        elif 'tools' in event_data:
                                            tool_msgs = event_data['tools'].get('messages', [])
                                            if tool_msgs:
                                                # We can show the tool output if desired, or just keep it hidden
                                                # For transparency, let's show a summary
                                                status.write("✅ Tool execution complete.")

                                except Exception as e:
                                    pass
                
                status.update(label="✅ Complete!", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                full_response = f"Sorry, I encountered an error: {str(e)}"

    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# Display Chat History
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Add PDF download button for assistant messages
        if message["role"] == "assistant":
            pdf_data = get_pdf_data(message["content"])
            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=f"itinerary_{i}.pdf",
                mime="application/pdf",
                key=f"download_{i}"
            )

