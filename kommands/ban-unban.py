from neonize.client import NewClient
from neonize.events import MessageEv
from whisp import is_owner, save_ban_users, ban_users, clean_number  

def register(commands):
    commands["ban"] = ban_user
    commands["unban"] = unban_user  

def ban_user(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    
    if len(args) < 1:
        client.reply_message("Por favor, proporciona el número del usuario a banear o el tag.", message)
        return
    
    user_input = args[0]
    user_to_ban = clean_number(user_input)  
    
    if user_to_ban in ban_users:
        client.reply_message(f"El usuario @{user_to_ban} ya está baneado.", message)
    else:
        ban_users.add(user_to_ban)
        save_ban_users(ban_users)
        client.reply_message(f"Usuario @{user_to_ban} ha sido baneado.", message)

def unban_user(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    if not is_owner(sender):
        client.reply_message("Lo siento, solo los owners pueden usar este comando.", message)
        return
    
    if len(args) < 1:
        client.reply_message("Por favor, proporciona el número del usuario a desbanear o el tag.", message)
        return
    
    user_input = args[0]
    user_to_unban = clean_number(user_input)  
    
    if user_to_unban not in ban_users:
        client.reply_message(f"El usuario @{user_to_unban} no está baneado.", message)
    else:
        ban_users.remove(user_to_unban)
        save_ban_users(ban_users)
        client.reply_message(f"Usuario @{user_to_unban} ha sido desbaneado.", message)
