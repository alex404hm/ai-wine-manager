import ollama
import json
# Choose a chat-capable model (ensured it is pulled)
model_name = 'gemma:2b'

with open("data/data.json", "r", encoding="utf-8") as f:
    user_data = json.load(f)

# Initialize conversation with a system prompt (optional) and a user message
messages = [
    {"role": "system", "content": f"""
     You are an Wine ai professional you can talk about anything in wine.
     If the user ask about what do you think i will like or what something the wine the user have then use this data: {user_data}
     """},
    {"role": "user", "content": "Hello!"},
]
# First response from the bot
response = ollama.chat(model=model_name, messages=messages)
print("Bot:", response.message.content)

# Continue the conversation:
while True:
    user_input = input("You: ")
    if not user_input:
        break  # exit loop on empty input
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content
    print("Bot:", answer)
    messages.append({"role": "assistant", "content": answer})