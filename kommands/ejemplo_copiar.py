# Ejemplo de mensaje con botón interactivo para copiar texto. Edita el texto dentro de comillas.
from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)

def copy(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    
    interactive_message = Message(
        viewOnceMessage=FutureProofMessage(
            message=Message(
                messageContextInfo=MessageContextInfo(
                    deviceListMetadata=DeviceListMetadata(),
                    deviceListMetadataVersion=2,
                ),
                interactiveMessage=InteractiveMessage(
                    body=InteractiveMessage.Body(text="Con este boton podrás copiar un mensaje"), # Mensaje en general que se enviará. 
                    footer=InteractiveMessage.Footer(text="@KomodoBot-Py"), # Marca de agua (Puedes Cambiarlo)
                    header=InteractiveMessage.Header(
                        title="Copia el mensaje 📝", # Titulo del mensaje. Esto saldrá primero.
                        subtitle="null",
                        hasMediaAttachment=False,
                    ),
                    nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                        buttons=[
                            InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                name="cta_copy",
                                buttonParamsJSON='{"display_text":"📝COPIAR TEXTO📝","id":"123456789","copy_code":"📝TEXTO QUE SE COPIARÁ📝"}', # Cambia los valores en mayuscula
                            ), # display_text es el texto que sale en el boton. copy_code es el texto a copiar.
                        ]
                    ),
                ),
            )
        )
    )
    
    client.send_message(chat, interactive_message)

def register(commands):
    commands["copiar"] = copy #Acá se define el comando, cambialo por el que tu quieras, el prefijo se añade automaticamente y puedes cambiarlo en "config.py" en la parte de prefix.
