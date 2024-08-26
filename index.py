import logging
import signal
import sys
from neonize.client import NewClient
from neonize.events import ConnectedEv, PairStatusEv

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def interrupted(*_):
    log.info("Bot interrumpido")
    sys.exit(0)

signal.signal(signal.SIGINT, interrupted)

# Crear la sesión 
client = NewClient("komodo_session.sqlite3")

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    log.info("✧━━━━━━ KOMODO BOT PY 🌅 ━━━━━━✧ ------------------------------------------------------------------ LISTO, BOT CONECTADO CON EXITO!! ✅")
    
    # Enviar un mensaje automático al conectarse
    client.send_message("50557418454@s.whatsapp.net", "El bot se ha conectado correctamente.")

@client.event(PairStatusEv)
def on_pair_status(client: NewClient, event: PairStatusEv):
    log.info(f"Emparejado como {event.ID.User}")

import whisp
whisp.initialize(client)

client.connect()
