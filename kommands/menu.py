from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["menu"] = menu
    commands["help"] = menu

def menu(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    push_name = message.Info.Pushname 

    greeting = f"¡Hola, {push_name}! 👋\nEstos son los comandos disponibles\n\n"

    menu_message = (
        f"┌────︶.︶.︶.︶.︶.︶.︶.︶ ୭̥⋆*｡\n"
        "✧ ₊ ˚ ✩ *KomodoBot-Py 🌅*\n"
        "✧ ₊ ˚ ✩ *Versión:* 1.0.2\n"
        f"✧ ₊ ˚ ✩ ╰────︶.︶ ⸙ ͛ ͎ ͛  ︶.︶ ✧ ₊ ˚ ✩,\n{greeting}"
        "✎｡｡｡ *Comandos de ejemplo:*\n"
        "⿻ /hola\n"
        "⿻ /bot (texto)\n"
        "⿻ /boton\n"
        "⿻ /copiar\n"
        "⿻ /imagen\n\n"
        "*✎｡｡｡ Comandos Generales:*\n"
        "⿻ /ping\n"
        "⿻ /dado\n"
        "⿻ /sticker\n"
        "⿻ /on /off\n"
        "⿻ /ban (@tag) /unban (@tag)\n"
        "⿻ /seguir\n"
        "⿻ /notify\n\n"                        
        "Nuevas funciones generales se añadirán próximamente..."
    )

    client.send_message(chat, menu_message)
