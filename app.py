import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_response(user_input):
    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title("model A - Chatbot")

# the below snippet is for Initializing the  session state for storing the chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Text input field for the user to type a message
user_input = st.text_input("Type your message:", key="user_input")


if st.button("Send"):
    if user_input:
        # Adding user's message to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})

        
        response = get_openai_response(user_input)

        # Adding GPT-4's response to session state
        st.session_state["messages"].append({"role": "assistant", "content": response})

# Display chat history
if st.session_state["messages"]:
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Bot:** {message['content']}")

# reset button to clear chat
if st.button("Clear Chat"):
    st.session_state["messages"] = []
