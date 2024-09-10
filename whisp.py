import logging
import importlib
import pkgutil
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.utils.message import get_message_type
import json
import os
import config

commands = {}
komodo_key = None  

parta = "38"
partb = "k-"
partc = "26"
partd = "50"
parte = "84"

def build_komodo_key():
    parts = [partb, parta, partc, partd, parte]
    return ''.join([parts[i] for i in range(len(parts))])

complete_komodo_key = build_komodo_key()

komodo_key_path = os.path.join('datamedia', 'komodokey.json')
chat_states_path = os.path.join('datamedia', 'chat_states.json')

# Guardar la KomodoKey en un archivo JSON
def save_komodo_key(key):
    os.makedirs(os.path.dirname(komodo_key_path), exist_ok=True)
    with open(komodo_key_path, 'w') as file:
        json.dump({"komodo_key": key}, file)

# Cargar la KomodoKey desde el archivo JSON
def load_komodo_key():
    if not os.path.exists(komodo_key_path):
        return None

    try:
        with open(komodo_key_path, 'r') as file:
            data = json.load(file)
            return data.get("komodo_key")
    except json.JSONDecodeError:
        logging.error("Error al leer el archivo JSON: contenido no válido.")
        return None
    except Exception as e:
        logging.error(f"Error al cargar la KomodoKey: {e}")
        return None

# Guardar el estado de los chats en el archivo JSON
def save_chat_states():
    os.makedirs(os.path.dirname(chat_states_path), exist_ok=True)
    with open(chat_states_path, 'w') as file:
        json.dump(chat_states, file)

# Cargar el estado de los chats desde el archivo JSON
def load_chat_states():
    if not os.path.exists(chat_states_path):
        return {}

    try:
        with open(chat_states_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error("Error al leer el archivo JSON de estados de chat: contenido no válido.")
        return {}
    except Exception as e:
        logging.error(f"Error al cargar el estado de los chats: {e}")
        return {}

chat_states = load_chat_states()

# Comando para activar el bot en un chat específico
def turn_on(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  
    chat_states[chat_id] = "on"  # Establece el estado del chat en "on"
    save_chat_states() 
    client.reply_message("El bot ha sido activado en este chat.", message)

# Comando para desactivar el bot en un chat específico
def turn_off(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  # Convertir el chat a un string
    chat_states[chat_id] = "off"  # Establece el estado del chat en "off"
    save_chat_states()  # Guardar el estado de chat (actualizado)
    client.reply_message("El bot ha sido desactivado en este chat.", message)

# Cargar los comandos disponibles
def load_commands():
    for _, module_name, _ in pkgutil.iter_modules(['kommands']):
        module = importlib.import_module(f'kommands.{module_name}')
        if hasattr(module, 'register'):
            module.register(commands)

    for _, module_name, _ in pkgutil.iter_modules(['datamedia/comandos_de_prueba']):
        module = importlib.import_module(f'datamedia.comandos_de_prueba.{module_name}')
        if hasattr(module, 'register'):
            module.register(commands)

# Función que maneja los mensajes recibidos
def handler(client: NewClient, message: MessageEv):
    global komodo_key
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  # Convertir el chat a un string
    sender = message.Info.MessageSource.Sender.User  # Número de teléfono del remitente
    is_group = message.Info.MessageSource.IsGroup  # Identificar si es enviado en un grupo
    msg_type = get_message_type(message)
    
    # Procesar el comando ON/OFF
    for prefix in config.PREFIXES:
        if text.startswith(f"{prefix}on"):
            turn_on(client, message, [], is_group, sender)
            return
        elif text.startswith(f"{prefix}off"):
            turn_off(client, message, [], is_group, sender)
            return

    # Verificar el OFF
    if chat_id in chat_states and chat_states[chat_id] == "off":
        logging.info(f"El bot está desactivado en el chat: {chat_id}")
        return  

    if komodo_key is None:
        komodo_key = load_komodo_key()

    if text and text[0] in config.PREFIXES:
        for prefix in config.PREFIXES:
            if text.startswith(f"{prefix}key"):
                key = text.split(" ")[1]
                if key == complete_komodo_key:
                    komodo_key = key
                    save_komodo_key(komodo_key)
                    client.reply_message("*KomodoKey definida correctamente! ✅*", message)
                else:
                    client.reply_message("*KomodoKey incorrecta!!*", message)
                return

        if komodo_key is None:
            client.reply_message("*Por favor, define la KomodoKey con /key [tu_clave] para usar comandos.*\n\n*Puedes pedirla a:*\n*Mi creador:* wa.me/50557418454\n*Grupo Oficial:* https://chat.whatsapp.com/EnkVyluXN2rDtrCekiYxxD", message)
            return

        command = text.split(" ")[0][1:]  
        args = text.split(" ")[1:]

        if command in commands:
            commands[command](client, message, args, is_group, sender)  
            config.commands_processed += 1
        else:
            client.reply_message(f"Lo siento, comando /{command} no encontrado!", message)
            logging.info(f"Comando no encontrado: {command}")
    else:
        logging.info(f"Mensaje recibido sin prefijo: {text}")

load_commands()

# Inicializar el cliente con los eventos necesarios
def initialize(client):
    # Handler de mensajes
    @client.event(MessageEv)
    def on_message(client: NewClient, message: MessageEv):
        handler(client, message)

    def download_media(client: NewClient, url: str, media_type: str):
        if media_type == "image":
            return get_bytes_from_name_or_url(url, MediaType.IMAGE)
        elif media_type == "video":
            return get_bytes_from_name_or_url(url, MediaType.VIDEO)
        elif media_type == "audio":
            return get_bytes_from_name_or_url(url, MediaType.AUDIO)
