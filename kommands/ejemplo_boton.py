from neonize.client import NewClient
from neonize.events import MessageEv
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)

def boton(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    interactive_message = Message(
        viewOnceMessage=FutureProofMessage(
            message=Message(
                messageContextInfo=MessageContextInfo(
                    deviceListMetadata=DeviceListMetadata(),
                    deviceListMetadataVersion=2,
                ),
                interactiveMessage=InteractiveMessage(
                    body=InteractiveMessage.Body(text="Haz clic en el botón para utilizar la función"),  # Mensaje en general que se enviará
                    footer=InteractiveMessage.Footer(text="@KomodoBot-Py"),  # Marca de agua
                    header=InteractiveMessage.Header(
                        title="Responder al mensaje 📩",  # Título del mensaje
                        subtitle="Selecciona una opción",
                        hasMediaAttachment=False,
                    ),
                    nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                        buttons=[
                            InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                name="reply_message",
                                buttonParamsJSON='{"display_text":"💬TEXTO DEL BOTON💬","id":"/hola"}',  # Texto de los botones, edita la parte de "/hola" con el comando que quieres que active el boton al ser utilizado 
                            ),
                        ]
                    ),
                ),
            )
        )
    )
    
    client.send_message(chat, interactive_message)

def register(commands):
    commands["boton"] = boton  # Define el comando, puedes cambiar el prefijo en config.py
