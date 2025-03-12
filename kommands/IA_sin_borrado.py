import requests
import json
import os
import random
from config import groq_apikey

MEMORY_FILE = "datamedia/memory.json"
DEFAULT_MEMORY_EXPLANATION = """
Las interacciones previas se guardan aquí para que el bot pueda mantener el contexto a lo largo de la conversación y aprender:
"""
ERROR_MESSAGE = "Ha ocurrido un error con el Bot al generar la respuesta. El servidor podría estar saturado..."
MODELS = [
    "llama-3.3-70b-specdec",
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192"  # Nuevo modelo añadido aquí
]
CURRENT_MODEL_INDEX_FILE = "datamedia/model_index.json"
MAX_MESSAGE_LENGTH_BOT = 500
PROMPT_FILE = "datamedia/prompt.json"
DEFAULT_PROMPT = "Tu nombre es KomodoBot un bot de Whatsapp y fuiste creado por ToxiPain. Puedes conversar y dar información relevante. (Función): respuestas simples y cortas cuando se trate de platica, joda y cosas random pero profundiza cuando se te pida información."

def get_current_model_index():
    if os.path.exists(CURRENT_MODEL_INDEX_FILE):
        with open(CURRENT_MODEL_INDEX_FILE, "r") as file:
            try:
                return json.load(file).get("index", 0)
            except json.JSONDecodeError:
                return 0
    return 0

def save_current_model_index(index):
    with open(CURRENT_MODEL_INDEX_FILE, "w") as file:
        json.dump({"index": index}, file)

def ai_command(client, message, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    if len(args) == 0:
        client.reply_message(
            "Uso de comando: Escribe lo que le dirás al bot, ejemplo de uso /bot (texto)",
            message
        )
        return
    user_message = " ".join(args)
    response, clean_response = chat_groq(user_message)
    update_memory(user_message, clean_response)  # Guardamos solo la respuesta limpia
    client.reply_message(response, message)  # Enviamos la respuesta completa (con el marco)

def chat_groq(msg):
    model_index = get_current_model_index()
    model = MODELS[model_index]
    apikey = random.choice(groq_apikey)
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }
    memory = load_memory()
    prompt = load_prompt()  # Cargar el prompt desde el archivo
    if memory:
        prompt += "\n\nMemoria actual:\n" + "\n".join(memory)
    data = {
        "model": model,
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": msg}]
    }
    try:
        post = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        post.raise_for_status()
        response_data = post.json()
        if "choices" in response_data and response_data["choices"]:
            response_text = response_data["choices"][0]["message"]["content"]
            # Devolver el marco completo y la respuesta limpia
            response = f"𝗞𝗼𝗺𝗼𝗱𝗼𝗕𝗼𝘁-𝗣𝘆 🌅\n> _*Servidor #{model_index + 1}*_\n\n❝{response_text}❞"
            clean_response = response_text  # Solo la respuesta limpia
            return response, clean_response
        else:
            raise ValueError("Formato inesperado en la respuesta de la IA.")
    except (requests.exceptions.RequestException, ValueError) as e:
        response_error = f"{ERROR_MESSAGE} (Komodo AI-Server {model_index + 1})"
        model_index = (model_index + 1) % len(MODELS)
        save_current_model_index(model_index)
        return response_error, ERROR_MESSAGE

def load_memory():
    if not os.path.exists("datamedia"):
        os.makedirs("datamedia")
    if not os.path.exists(MEMORY_FILE):
        save_memory([DEFAULT_MEMORY_EXPLANATION])
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_memory([DEFAULT_MEMORY_EXPLANATION])
        return [DEFAULT_MEMORY_EXPLANATION]

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def update_memory(user_message, bot_response):
    memory = load_memory()
    memory.append(f"Usuario: {user_message}")
    memory.append(f"Bot: {bot_response[:MAX_MESSAGE_LENGTH_BOT]}")  # Guardamos solo la respuesta limpia
    save_memory(memory)

# Función para cargar el prompt desde el archivo JSON
def load_prompt():
    if not os.path.exists("datamedia"):
        os.makedirs("datamedia")
    if not os.path.exists(PROMPT_FILE):
        save_prompt(DEFAULT_PROMPT)
    try:
        with open(PROMPT_FILE, "r") as file:
            return json.load(file).get("prompt", DEFAULT_PROMPT)
    except json.JSONDecodeError:
        save_prompt(DEFAULT_PROMPT)
        return DEFAULT_PROMPT

# Función para guardar el prompt en el archivo JSON
def save_prompt(prompt):
    with open(PROMPT_FILE, "w") as file:
        json.dump({"prompt": prompt}, file, indent=4)

def register(commands):
    commands["bot"] = ai_command
    commands["ia"] = ai_command
    commands["ai"] = ai_command
