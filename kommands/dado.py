import random
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["dado"] = dado 

def dado(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    messages = ["1", "2", "3", "4", "5", "6"] # Acá se definen las variables que se elegiran aleatoriamente, puedes cambiarlo por texto o lo que quieras.
    
    random_message = random.choice(messages)
    
    client.reply_message(f"El resultado del dado es: {random_message}", message)
