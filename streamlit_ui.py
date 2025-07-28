

import streamlit as st
import requests


#API_URL = "http://127.0.0.1:8000/chat/"
API_URL = "https://virtual-friend.onrender.com/chat/"
SESSION_ID = "streamlit_user_001"



# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Virtual Friend")

st.title("Virtual Friend")

# Send message logic in a callback
def send_message():
    user_input = st.session_state.user_input
    if not user_input.strip():
        return

    # Call FastAPI
    response = requests.post(API_URL, json={
        "session_id": SESSION_ID,
        "prompt": user_input
    })

    if response.status_code == 200:
        bot_reply = response.json()["response"]

        # Append to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Virtual Friend",bot_reply))

        # Reset input by clearing the value before next rerun
        st.session_state.user_input = ""
    else:
        st.error(f"API Error: {response.text}")

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**{sender}:** {msg}")
    else:
        st.markdown(f"**{sender}:** {msg}")

# Input field tied to session_state
st.text_input("You:", key="user_input", on_change=send_message)

