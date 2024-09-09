from neonize.client import NewClient
from neonize.events import MessageEv

def convert_to_sticker(client: NewClient, message: MessageEv, args: list, is_group: bool):
    chat = message.Info.MessageSource.Chat
    # Suponiendo que la imagen es enviada como una URL
    if args:
        image_url = args[0]
        client.send_sticker(
            chat,
            image_url,
            name="Sticker",
            packname="Test"
        )
    else:
        client.reply_message("Por favor, proporciona la URL de la imagen.", message)

def register(commands: dict):
    commands['s'] = convert_to_sticker
    commands['sticker'] = convert_to_sticker
