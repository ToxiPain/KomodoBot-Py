from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["menu"] = menu

def menu(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    client.send_message(chat, "┌────︶.︶.︶.︶.︶.︶.︶.︶ ୭̥⋆*｡\n ੈ₊˚༅༴│↷◌⁺˖ *KomodoBot-Py 🌅*\n ੈ₊˚༅༴│↷◌⁺˖ *Versión:* 1.0.2\n\n*✎｡｡｡ Comandos de ejemplo:*\n⿻ /hola\n⿻ /ia\n⿻ /boton\n⿻ /copiar\n⿻ /imagen\n\n*✎｡｡｡ Comandos Generales:*\n⿻ /ping") 
  
