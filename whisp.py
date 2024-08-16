import logging
import importlib
import pkgutil
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.utils.message import get_message_type
from PIL import Image
from io import BytesIO
import json
import config 

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
    
    if text and text[0] in config.PREFIXES:  
        command = text.split(" ")[0][1:]
        args = text.split(" ")[1:]

        if command in commands:
            commands[command](client, message, args)
        else:
            # Enviar mensaje de comando no encontrado
            client.reply_message("Lo siento, comando no encontrado!", message)
            logging.info(f"Comando no encontrado: {command}")
    else:
        logging.info(f"Mensaje recibido sin prefijo: {text}")

load_commands()

def initialize(client):
    # Handler client
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

    def remove_background(client: NewClient, message: MessageEv, chat, image_message):
        img_data = image_message.imageMessage.jpegThumbnail
        img = Image.open(BytesIO(img_data))
        img = img.convert("RGBA")
        new_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
        img = Image.alpha_composite(new_img, img)
        output = BytesIO()
        img.save(output, format="PNG")
        client.send_message(chat, client.build_image_message(output.getvalue(), "Background removed"))
