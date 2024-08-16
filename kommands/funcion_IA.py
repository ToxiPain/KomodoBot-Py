import requests, random
from config import groq_apikey

def ai_command(client, message, args):
    chat = message.Info.MessageSource.Chat
    
    if len(args) == 0:
        client.reply_message("Uso de comando: Escribe lo que le dirás al bot, ejemplo de uso /bot (texto)", message)
        return
    
    user_message = " ".join(args)
    response = chat_groq(user_message)
    client.reply_message(response, message)

def chat_groq(msg):
    apikey = random.choice(groq_apikey)
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }
# Acá podrás editar cual quieres que sea la indicación inicial de la IA
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
    commands["ia"] = ai_command
    commands["ai"] = ai_command
