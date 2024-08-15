import logging
import importlib
import pkgutil
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.utils.message import get_message_type
from PIL import Image
from io import BytesIO
import json

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
    if text and text[0] in PREFIXES:
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

def initialize(client):
    # Ahora inicializamos el handler sin modificar el cliente
    @client.event(MessageEv)
    def on_message(client: NewClient, message: MessageEv):
        handler(client, message)

    # Funciones adicionales (incluyendo todas del script base original)
    def send_image(client: NewClient, chat, image_path, caption=""):
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
        client.send_message(chat, client.build_image_message(img_data, caption))

    def reply_message(client: NewClient, chat, original_message, reply_text):
        client.reply_message(reply_text, original_message)

    def send_interactive_message(client: NewClient, chat, body, buttons, footer="@brutalx-04"):
        client.send_message(
            chat,
            Message(
                viewOnceMessage=FutureProofMessage(
                    message=Message(
                        messageContextInfo=MessageContextInfo(
                            deviceListMetadata=DeviceListMetadata(),
                            deviceListMetadataVersion=2,
                        ),
                        interactiveMessage=InteractiveMessage(
                            body=InteractiveMessage.Body(text=body),
                            footer=InteractiveMessage.Footer(text=footer),
                            header=InteractiveMessage.Header(
                                hasMediaAttachment=True,
                                imageMessage=client.build_image_message("src/image/bg.jpg").imageMessage
                            ),
                            nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                                buttons=[
                                    InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                        name=btn["title"],
                                        buttonParamsJSON=json.dumps({"display_text": btn["description"], "id": btn["id"]})
                                    ) for btn in buttons
                                ]
                            ),
                        ),
                    )
                )
            )
        )

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

    def fetch_content(client: NewClient, url: str):
        if "tiktok" in url:
            return {"status": "success", "type": "video", "content": "TikTok video content"}
        elif "instagram" in url:
            return {"status": "success", "type": "image", "content": "Instagram image content"}
