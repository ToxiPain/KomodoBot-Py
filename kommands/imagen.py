from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["imagen"] = imagen # Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente y puedes cambiarlo en "config.py" en la parte de prefix.

def imagen(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    # Ruta de la imagen a enviar
    image_path = "datamedia/komodo.png"
    
    # Enviar la imagen al chat
    client.send_image(
        chat,
        image_path,
        caption="Imagen de KomodoBot!",
        quoted=message,  # Esto citará el mensaje original
    )
