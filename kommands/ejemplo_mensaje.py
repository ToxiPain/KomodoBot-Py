# Ejemplo de envio de mensaje simple. Edita el texto dentro de comillas.
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["hola"] = hola #Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente y puedes cambiarlo en "config.py" en la parte de prefix.

def hola(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    client.send_message(chat, "Hola soy KomodoBot!") # Acá cambias lo que quieres que diga el bot
    
# Puedes cambiar client.send_message a client.reply_message para que pase de simplemente mandar texto plano a contestar el mensaje del comando.
