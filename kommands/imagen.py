# Ejemplo de envio de imagenes. Edita el texto dentro de comillas.
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["imagen"] = imagen #Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente y puedes cambiarlo en "config.py" en la parte de prefix.

def imagen(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    # Ruta de la imagen a enviar
    image_path = "datamedia/komodo.png" # Cambia la imagen por el nombre de la imagen que vas a utilizar, tu imagen en cuestión deberá estar dentro de la carpeta "datamedia".
    
    # Envio de la imagen:
    client.send_image(
        chat,
        image_path,
        caption="Imagen de KomodoBot!", # Texto que envia junto con la imagen
        quoted=message,  # Elimina esto si no quieres que cite el mensaje original
    )
