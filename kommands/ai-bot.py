import requests, random
from config import groq_apikey

def ai_command(client, message, args):
    chat = message.Info.MessageSource.Chat
    
    # Verificar si el usuario no ha proporcionado ningún texto después del comando /ai
    if len(args) == 0:
        client.send_message(chat, "Uso de comando: Escribe lo que le dirás al bot, ejemplo de uso /ai (texto)")
        returns
    
    user_message = " ".join(args)
    response = chat_groq(user_message)
    client.send_message(chat, response)

def chat_groq(msg):
    apikey = random.choice(groq_apikey)
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }

    prompt = "Hola tu serás un bot de whatsapp, podrás conversar y entretener. Tu nombre es KomodoBot y fuiste creado por ToxiPain"

    data = {
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": msg,
            }
        ],
        "model": "llama3-8b-8192"
    }

    post = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data).json()

    return post["choices"][0]["message"]["content"]

def register(commands):
    commands["bot"] = ai_command
