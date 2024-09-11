from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)

def register(commands):
    commands["menu"] = menu
    commands["help"] = menu

def menu(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    push_name = message.Info.Pushname
    is_group = message.Info.MessageSource.IsGroup
    
    group_name = ""
    
    if is_group:
        group_info = client.get_group_info(chat)
        group_name = group_info.GroupName.Name if group_info and group_info.GroupName else ""
    
    greeting = f"¡Hola, {push_name}! 👋\nEstos son los comandos disponibles\n\n"
    
    menu_message = (
        f"┌────︶.︶.︶.︶.︶.︶.︶.︶ ୭̥⋆*｡\n"
        "✧ ₊ ˚ ✩ *KomodoBot-Py 🌅*\n"
        "✧ ₊ ˚ ✩ *Versión:* 1.0.2\n"
        f"{f'✧ ₊ ˚ ✩ *Grupo:* {group_name}' if is_group else '✧ ₊ ˚ C H A T   P R I V A D O'}\n"  
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
        "⿻ /notify\n"                        
        "⿻ *********"
    )

    client.send_message(
        chat,
        Message(
            viewOnceMessage=FutureProofMessage(
                message=Message(
                    messageContextInfo=MessageContextInfo(
                        deviceListMetadata=DeviceListMetadata(),
                        deviceListMetadataVersion=2,
                    ),
                    interactiveMessage=InteractiveMessage(
                        body=InteractiveMessage.Body(text=menu_message),
                        footer=InteractiveMessage.Footer(text="Nuevas funciones generales se añadirán próximamente..."),
                        header=InteractiveMessage.Header(
                            title="",
                            subtitle="",
                            hasMediaAttachment=False,
                        ),
                        nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                            buttons=[
                                InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                    name="cta_call",
                                    buttonParamsJSON='{"display_text":"Menu de KomodoBot-Py","id":"000"}',
                                ),
                            ]
                        ),
                    ),
                )
            )
        ),
    )

    reaction(client, chat, message, "✅️")

def reaction(client: NewClient, chat, message, emoji):
    try:
        client.send_message(
            chat,
            client.build_reaction(
                chat,
                sender=message.Info.MessageSource.Sender,
                message_id=message.Info.ID,
                reaction=emoji
            ),
        )
    except Exception as e:
        print(f"Error al reaccionar al mensaje: {e}")
