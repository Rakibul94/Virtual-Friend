

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Literal
import ollama

app = FastAPI()

client = ollama.Client()

# class PromptRequest(BaseModel):
#     prompt: str
#     model: str = "llama3.2:1b"  # Optional default

# @app.post("/generate/")
# def generate_response(request: PromptRequest):
#     try:
#         response = client.generate(model=request.model, prompt=request.prompt)
#         return {"response": response["response"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# In-memory session storage (key: session_id, value: list of messages)
session_memory: Dict[str, List[Dict[str, str]]] = {}

# Request schema
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    model: str = "llama3.2:1b"

@app.post("/chat/")
def chat(request: ChatRequest):
    try:
        # Initialize message history if session is new
        if request.session_id not in session_memory:
            session_memory[request.session_id] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        
        # Add user's message
        session_memory[request.session_id].append({
            "role": "user",
            "content": request.prompt
        })

        # Call the model with full conversation
        response = client.chat(
            model=request.model,
            messages=session_memory[request.session_id]
        )

        # Add assistant response to history
        assistant_reply = response["message"]["content"]
        session_memory[request.session_id].append({
            "role": "assistant",
            "content": assistant_reply
        })

        return {"response": assistant_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
