


import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat/"
SESSION_ID = "gradio_user_001"  # Could be dynamic if needed

# Store full conversation for display
chat_history = []

def chat_with_api(user_input):
    global chat_history

    # Call FastAPI endpoint
    response = requests.post(API_URL, json={
        "session_id": SESSION_ID,
        "prompt": user_input
    })

    if response.status_code != 200:
        return "❌ Error from API: " + response.text, chat_history

    reply = response.json()["response"]

    # Append to history for Gradio display
    chat_history.append(("You", user_input))
    chat_history.append(("Virtual Friend", reply))

    return "", chat_history

# Create Gradio interface
chatbot_ui = gr.Interface(
    fn=chat_with_api,
    inputs=gr.Textbox(placeholder="Type a message...", label="You"),
    outputs=[
        gr.Textbox(visible=False),  # Dummy output to suppress empty string return
        gr.Chatbot()
    ],
    title="Virtual Friend",
    live=False
)

if __name__ == "__main__":
    chatbot_ui.launch(share=True)
