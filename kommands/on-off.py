from neonize.client import NewClient
from neonize.events import MessageEv
import json
import os

from whisp import chat_states, save_chat_states

def register(commands):
    commands["on"] = turn_on
    commands["off"] = turn_off

def turn_on(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  
    chat_states[chat_id] = "on" 
    save_chat_states()  
    client.reply_message("El bot ha sido activado en este chat. ✔", message)

def turn_off(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)  
    chat_states[chat_id] = "off"  
    save_chat_states()  
    client.reply_message("El bot ha sido desactivado en este chat. ❌", message)
