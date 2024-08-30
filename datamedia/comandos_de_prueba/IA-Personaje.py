import asyncio
from characterai import aiocai
from neonize.client import NewClient
from neonize.events import MessageEv

# Reemplaza 'TU_TOKEN' con tu token de CharacterAI
TOKEN = '11749093f433716cdf23943b4b1f7ef58ac3271e'

def register(commands):
    commands["try"] = test_command  # El comando se define aquí
    commands["t"] = test_command  # El comando se define aquí

async def interact_with_characterai(char_id, message_text):
    client = aiocai.Client(TOKEN)
    me = await client.get_me()

    async with await client.connect() as chat:
        new, answer = await chat.new_chat(char_id, me.id)

        # Enviar el mensaje recibido al Character AI
        message = await chat.send_message(char_id, new.chat_id, message_text)
        
        # Retornar la respuesta del Character AI
        return f'{message.name}: {message.text}'

def test_command(client: NewClient, message: MessageEv, args):
    char_id = "vdP72Co12azBgsQJ8xus_UZE1VAF-_Olnkt6u3kedrM"  # Reemplaza con el ID del CharacterAI
    chat = message.Info.MessageSource.Chat
    
    if args:
        user_message = ' '.join(args)
    else:
        # Si no se proporcionan argumentos, enviar un mensaje de uso correcto
        usage_message = "Uso correcto: testeo [mensaje] - Envía el mensaje a Tatsumaki."
        client.reply_message(usage_message, message)
        return
    
    # Crear una tarea asíncrona para manejar la interacción
    async def run_interaction():
        response = await interact_with_characterai(char_id, user_message)
        client.reply_message(response, message)
    
    # Ejecutar la tarea en el hilo principal de asyncio
    asyncio.run(run_interaction())
