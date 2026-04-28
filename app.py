import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    st.error("API key not found. Please add MISTRAL_API_KEY in .env file")
    st.stop()

# API Configuration
API_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# Streamlit Page Setup
st.set_page_config(page_title="Mistral AI Chatbot")

st.title("🤖 AI Chatbot using Mistral 7B")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Ask something...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Create API Payload
    payload = {
        "model": "open-mistral-7b",
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    try:

        # Send API Request
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload
        )

        if response.status_code == 200:

            data = response.json()

            reply = data["choices"][0]["message"]["content"]

        else:
            reply = f"Error: {response.text}"

    except Exception as e:
        reply = f"Request Failed: {str(e)}"

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save Assistant Message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })