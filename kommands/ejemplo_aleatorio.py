# Ejemplo de envio de mensaje con funciones aleatorias. 
import random
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["dado"] = dado # Acá se cambia el prefijo.

def dado(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    messages = ["1", "2", "3", "4", "5", "6"] # Acá se definen las variables que se elegiran aleatoriamente, puedes cambiarlo por texto o lo que quieras que el bot mande de forma aleatoria.
    
    resultado = random.choice(messages)
    
    client.reply_message(f"El resultado del dado es: {resultado} 🎲", message) # Mensaje que manda + el resultado que se cambiará por {resultado}. 
