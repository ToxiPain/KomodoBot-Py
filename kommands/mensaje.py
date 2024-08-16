from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["hola"] = hola #Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente.

def hola(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    client.send_message(chat, "Hola soy KomodoBot!") # Acá cambias lo que quieres que diga el bot
# send_message - Para que simplemente envie texto Plano
# reply_message - Puedes añadirlo para que conteste al mensaje del comando.
