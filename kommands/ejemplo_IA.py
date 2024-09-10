# Comando de ejemplo de ChatBot simple con inteligencia artificial editable con tareas simples. Edita lo que esta dentro de comillas "".
import requests, random
from config import groq_apikey

def ai_command(client, message, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    
    if len(args) == 0:
        client.reply_message("Uso de comando: Escribe lo que le dirás al bot, ejemplo de uso /bot (texto)", message) # Esto enviará en caso de que no se añada texto luego del comando. 
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
# Acá podrás editar cual quieres que sea la indicación inicial de la IA:
    prompt = "Tu nombre es KomodoBot y fuiste creado por ToxiPain. Puedes conversar y dar información relevante." 

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
    commands["bot"] = ai_command # Puedes cambiar estos prefijos por los que quieras o eliminar los sobrantes. 
    commands["ia"] = ai_command
    commands["ai"] = ai_command
