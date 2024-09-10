# Ejemplo de envio de mensaje con funciones aleatorias. Edita el texto dentro de comillas.
import random
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["dado"] = dado #Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente y puedes cambiarlo en "config.py" en la parte de prefix.

def dado(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    
    messages = ["1", "2", "3", "4", "5", "6"] # Acá se definen las variables que se elegiran aleatoriamente, puedes cambiarlo por texto o lo que quieras que el bot mande de forma aleatoria.
    
    resultado = random.choice(messages)
    
    client.reply_message(f"El resultado del dado es: {resultado} 🎲", message) # Mensaje que manda + el resultado que se cambiará por {resultado}. 
