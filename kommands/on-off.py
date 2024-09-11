from neonize.client import NewClient
from neonize.events import MessageEv
import json
import os
import config  

from whisp import chat_states, save_chat_states

def register(commands):
    commands["on"] = turn_on
    commands["off"] = turn_off

def is_owner(sender):
    return sender in config.OWNERS

def turn_on(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)
    chat_states[chat_id] = "on"
    save_chat_states()
    client.reply_message("El bot ha sido activado en este chat. ✔", message)

def turn_off(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    
    chat = message.Info.MessageSource.Chat
    chat_id = str(chat)
    chat_states[chat_id] = "off"
    save_chat_states()
    client.reply_message("El bot ha sido desactivado en este chat. ❌", message)
