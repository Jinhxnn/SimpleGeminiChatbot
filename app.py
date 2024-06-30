"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

#response = chat_session.send_message("INSERT_INPUT_HERE")

#print(response.text)

import streamlit as st
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Simple Gemini ChatBot")


#Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def display_assistant_response_with_delay():
        # Display typing indicator or interim message
        st.markdown("Assistant is typing...")  # Show typing indicator or message

        
        time.sleep(0.5)  # Adjust the delay time in seconds

        # Get assistant's response
        assistant_response = chat_session.last.text

        st.markdown(assistant_response)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Added a button to clear the chat
with st.sidebar: 
    if st.button("Clear and Restart Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
        

    # Theme toggle button
    theme_options = ["Light Mode", "Dark Mode"]
    current_theme = st.selectbox("Select Theme:", theme_options)

    if current_theme == "Dark Mode":
        st.markdown("""
            <style>
            body {
                background-color: #1f2a38;
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            body {
                background-color: white;
                color: black;
            }
            </style>
        """, unsafe_allow_html=True)

    

# React to user input
if prompt := st.chat_input("Say something:"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    #response = f"Echo: {prompt}"
    
    # Send message to the model
    response = chat_session.send_message(prompt)

    # Display assistant response in chat message container
    display_assistant_response_with_delay()

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chat_session.last.text})

