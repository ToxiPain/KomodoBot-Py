from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["seguir"] = seguir_canal

def seguir_canal(client: NewClient, message: MessageEv, args):
    if len(args) < 1:
        client.reply_message("Por favor, proporciona el enlace del canal.", message)
        return
    
    canal_url = args[0]
    try:
        metadata = client.get_newsletter_info_with_invite(canal_url)
        err = client.follow_newsletter(metadata.ID)
        if err:
            client.reply_message(f"Error al seguir el canal: {err}", message)
        else:
            client.reply_message(f"El bot ha seguido el canal con éxito! ☑️📡", message)
    except Exception as e:
        client.reply_message(f"Hubo un error al intentar seguir el canal: {e}", message)
