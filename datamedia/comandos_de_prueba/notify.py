import time
from threading import Timer
from neonize.client import NewClient
from neonize.events import MessageEv

def register(commands):
    commands["notify"] = notify  # Define el comando, el prefijo se añade automáticamente.

def notify(client: NewClient, message: MessageEv, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat
    
    if len(args) < 2:
        client.send_message(chat, "Uso: /notify <mensaje> <tiempo> (ejemplo: /notify Hola 2m).\n\nFormatos Válidos: 1s, 1m, 1h.")
        return
    
    # Extraer mensaje y tiempo
    mensaje = " ".join(args[:-1])
    tiempo_str = args[-1]
    
    # Convertir tiempo a segundos
    tiempo_segundos = parse_time(tiempo_str)
    if tiempo_segundos is None:
        client.send_message(chat, "Formato de tiempo no válido. Usa formatos como 1s, 1m, 1h.")
        return
    
    # Función para enviar el aviso previo
    def aviso_previo():
        client.send_message(chat, f"*🔔 Aviso:* La notificación establecida se enviará en 5 segundos.")
    
    # Función para enviar el mensaje de notificación
    def enviar_notificacion():
        client.send_message(chat, f"*🛑--( Notificación: )--🛑*\n\n{mensaje}")

    # Programar el aviso previo
    tiempo_aviso = max(tiempo_segundos - 5, 0)
    Timer(tiempo_aviso, aviso_previo).start()

    # Programar el envío del mensaje
    Timer(tiempo_segundos, enviar_notificacion).start()

    # Enviar mensaje de confirmación
    client.send_message(chat, f"Notificación programada: '{mensaje}' en {tiempo_str}.")

def parse_time(tiempo_str):
    """Convierte un tiempo en formato '1s', '2m', '1h' a segundos."""
    try:
        if tiempo_str.endswith('s'):
            return int(tiempo_str[:-1])
        elif tiempo_str.endswith('m'):
            return int(tiempo_str[:-1]) * 60
        elif tiempo_str.endswith('h'):
            return int(tiempo_str[:-1]) * 3600
        else:
            return None
    except ValueError:
        return None
