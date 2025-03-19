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

chat_states_path = os.path.join('datamedia', 'chat_states.json')
ban_users_path = os.path.join('datamedia', 'ban_users.json')

def save_chat_states():
    os.makedirs(os.path.dirname(chat_states_path), exist_ok=True)
    with open(chat_states_path, 'w') as file:
        json.dump(chat_states, file)

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

def save_ban_users(ban_users):
    os.makedirs(os.path.dirname(ban_users_path), exist_ok=True)
    with open(ban_users_path, 'w') as file:
        json.dump(list(ban_users), file)

def load_ban_users():
    if not os.path.exists(ban_users_path):
        return set()
    try:
        with open(ban_users_path, 'r') as file:
            return set(json.load(file))
    except json.JSONDecodeError:
        logging.error("Error al leer el archivo JSON de usuarios baneados: contenido no válido.")
        return set()
    except Exception as e:
        logging.error(f"Error al cargar los usuarios baneados: {e}")
        return set()

chat_states = load_chat_states()
ban_users = load_ban_users()

def is_owner(sender):
    return sender in config.OWNERS

def is_banned(sender):
    return sender in ban_users

def clean_number(number):
    if number.startswith('@'):
        return number[1:]
    return number

def ban_user(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    if len(args) < 1:
        client.reply_message("Por favor, proporciona el número del usuario a banear o el tag.", message)
        return
    user_input = args[0]
    user_to_ban = clean_number(user_input)  
    if user_to_ban in ban_users:
        client.reply_message(f"El usuario {user_to_ban} ya está baneado.", message)
    else:
        ban_users.add(user_to_ban)
        save_ban_users(ban_users)
        client.reply_message(f"Usuario {user_to_ban} ha sido baneado.", message)

def turn_on(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  
    chat_states[chat_id] = "on"
    save_chat_states() 
    client.reply_message("El bot ha sido activado en este chat.", message)

def turn_off(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)
    chat_states[chat_id] = "off"
    save_chat_states()
    client.reply_message("El bot ha sido desactivado en este chat.", message)

def load_commands():
    for _, module_name, _ in pkgutil.iter_modules(['kommands']):
        module = importlib.import_module(f'kommands.{module_name}')
        if hasattr(module, 'register'):
            module.register(commands)
    for _, module_name, _ in pkgutil.iter_modules(['datamedia/comandos_de_prueba']):
        module = importlib.import_module(f'datamedia.comandos_de_prueba.{module_name}')
        if hasattr(module, 'register'):
            module.register(commands)

def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)
    sender = message.Info.MessageSource.Sender.User
    is_group = message.Info.MessageSource.IsGroup
    msg_type = get_message_type(message)
    if is_banned(sender):
        logging.info(f"Mensaje de usuario baneado {sender} ignorado.")
        return
    for prefix in config.PREFIXES:
        if text.startswith(f"{prefix}on"):
            turn_on(client, message, [], is_group, sender)
            return
        elif text.startswith(f"{prefix}off"):
            turn_off(client, message, [], is_group, sender)
            return
    if chat_id in chat_states and chat_states[chat_id] == "off":
        logging.info(f"El bot está desactivado en el chat: {chat_id}")
        return  
    if text and text[0] in config.PREFIXES:
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

def initialize(client):
    @client.event(MessageEv)
    def on_message(client: NewClient, message: MessageEv):
        handler(client, message)
