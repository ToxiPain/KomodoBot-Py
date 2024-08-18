from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["coño"] = comando_unico  # Define el comando, el prefijo se añade automáticamente.

def comando_unico(client: NewClient, message: MessageEv, args):
    chat = message.Info.MessageSource.Chat
    
    # Enviar un mensaje de texto
    client.send_message(
        chat,
        "Aquí tienes un mensaje con un archivo adjunto y una vista previa de enlace:"
    )
    
    # Enviar un documento PDF
    client.send_document(
        chat,
        "https://www.example.com/sample.pdf",
        caption="Aquí tienes un documento PDF.",
        filename="muestra.pdf"
    )
    
    # Enviar un mensaje con vista previa de enlace
    client.send_message(
        chat,
        "Visita este enlace para más información: https://github.com/krypton-byte/neonize",
        link_preview=True
    )
