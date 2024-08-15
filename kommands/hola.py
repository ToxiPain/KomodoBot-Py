def hola(client, message, args):
    chat = message.Info.MessageSource.Chat
    client.reply_message(chat, "Hola mundo", message)

def register(commands):
    commands["hola"] = hola