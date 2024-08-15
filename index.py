# index.py
import sys
import os
import logging
import signal
from neonize.client import NewClient
from whisp import handler
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,
)

from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata,
)
from neonize.types import MessageServerID
from neonize.utils import log
from neonize.utils.enum import ReceiptType

logging.basicConfig(level=logging.DEBUG)

def interrupted(*_):
    logging.info("El bot se ha detenido ❌.")
    exit(0)

signal.signal(signal.SIGINT, interrupted)

client = NewClient("KomodoBot_Session")

@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    logging.info("✅ Cliente Creado: Conectado con exito al servidor de Whatsapp ✅")

@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
    logging.debug(f"💬 Se ha recibido: {receipt}")

@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    logging.debug(f"📞 Llamada recibida: {call}")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)

@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    logging.info(f"👤 Logueado como: {message.ID.User}")

client.connect()