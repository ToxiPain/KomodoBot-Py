# whisp.py
import logging
import importlib
import pkgutil
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.utils.message import get_message_type

# Definición de prefijos permitidos
PREFIXES = ["/", ".", "#", "!"]

# Diccionario para almacenar los comandos
commands = {}

def load_commands():
    """Carga todos los módulos en la carpeta kommands y registra los comandos."""
    for _, module_name, _ in pkgutil.iter_modules(['kommands']):
        module = importlib.import_module(f'kommands.{module_name}')
        if hasattr(module, 'register'):
            module.register(commands)

def handler(client: NewClient, message: MessageEv):
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    msg_type = get_message_type(message)
    
    # Identificar el prefijo
    if text[0] in PREFIXES:
        command = text.split(" ")[0][1:]
        args = text.split(" ")[1:]

        # Ejecutar el comando si está registrado
        if command in commands:
            commands[command](client, message, args)
        else:
            logging.info(f"Comando no encontrado: {command}")
    else:
        logging.info(f"Mensaje recibido sin prefijo: {text}")

# Cargar todos los comandos al iniciar
load_commands()
