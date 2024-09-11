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
    commands["lista"] = list_buttons

def list_buttons(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat

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
                        body=InteractiveMessage.Body(text="Selecciona una opción:"),
                        footer=InteractiveMessage.Footer(text="Elige una opción de la lista."),
                        header=InteractiveMessage.Header(
                            title="Lista de Botones",
                            subtitle="Elige una opción",
                            hasMediaAttachment=False,
                        ),
                        nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
                            buttons=[
                                InteractiveMessage.NativeFlowMessage.NativeFlowButton(
                                    name="single_select",
                                    buttonParamsJSON='{"title":"Opciones","sections":[{"title":"Opciones","highlight_label":"Seleccione","rows":[{"header":"Opción 1","title":"Opción 1","description":"Descripción Opción 1","id":"option1"},{"header":"Opción 2","title":"Opción 2","description":"Descripción Opción 2","id":"option2"}]}]}',
                                )
                            ]
                        ),
                    ),
                )
            )
        ),
    )
