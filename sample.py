

import ollama

client = ollama.Client()

model = "llama3.2:1b"
# prompt = 'Act like you are Arthur Morgan from Red Dead:\nHello!'

# response = client.generate(model=model, prompt=prompt)

# print(response["response"])

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    # run the chain
    messages.append({"role": "user", "content": prompt})
    response = client.chat(model=model, messages=messages)
    print("Chatbot:", response["message"]["content"])