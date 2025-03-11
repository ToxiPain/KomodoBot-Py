import requests, random
import json
import os
from config import groq_apikey

# Definir la ruta del archivo JSON dentro de la carpeta 'datamedia'
MEMORY_FILE = "datamedia/memory.json"

# Definir el texto que será agregado como "explicación predeterminada" sobre la memoria
DEFAULT_MEMORY_EXPLANATION = """
Acá es donde se almacena la memoria acumulativa del bot.
Cada vez que el bot responde, las interacciones previas se guardan aquí para que el bot pueda mantener el contexto a lo largo de la conversación y aprender. El bot no repetirá estas interacciones, pero las usará como referencia para generar respuestas coherentes cuando las necesite.
"""

# Aquí puedes definir el mensaje de error que quieras que el bot responda
ERROR_MESSAGE = "Ha ocurrido un error al generar la respuesta. El servidor podría estar saturado..."

# Definir los modelos disponibles
MODELS = [
    "llama-3.3-70b-specdec",
    "llama-3.3-70b-versatile",
    "llama3-70b-8192"
]

# Configuración para limitar la memoria (puedes cambiar el número de interacciones o la longitud de los textos)
MAX_MESSAGE_LENGTH_BOT = 500  # Número máximo de caracteres para cada respuesta del bot guardada
MAX_INTERACTIONS_BEFORE_CLEAN = 50  # Número máximo de interacciones antes de borrar las primeras

def ai_command(client, message, args, is_group: bool, sender: str):
    chat = message.Info.MessageSource.Chat

    if len(args) == 0:
        client.reply_message(
            "Uso de comando: Escribe lo que le dirás al bot, ejemplo de uso /bot (texto)",
            message
        )  # Esto enviará en caso de que no se añada texto luego del comando.
        return

    user_message = " ".join(args)
    response = chat_groq(user_message)

    # Guardar la nueva interacción en la memoria
    update_memory(user_message, response)

    client.reply_message(response, message)


def chat_groq(msg):
    apikey = random.choice(groq_apikey)
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }

    # Cargar la memoria anterior
    memory = load_memory()

    # Crear el prompt con una introducción fija
    prompt = "Tu nombre es KomodoBot y fuiste creado por ToxiPain. Puedes conversar y dar información relevante. (Función): respuestas simples y cortas cuando se trate de platica, joda y cosas random pero profundiza cuando se te pida información."

    # Solo agregar la memoria (sin repetirla cada vez) como contexto
    if memory:
        prompt += "\n\nMemoria actual:\n" + "\n".join(memory)

    # Añadir el mensaje actual del usuario
    data = {
        "messages": [{
            "role": "system",
            "content": prompt
        }, {
            "role": "user",
            "content": msg,
        }]
    }

    # Rotación infinita entre los modelos
    while True:
        for i, model in enumerate(MODELS):
            try:
                data["model"] = model
                post = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                     headers=headers,
                                     json=data)

                # Comprobar si la solicitud fue exitosa (status code 200)
                post.raise_for_status()  # Lanza un error si la respuesta no es exitosa

                # Verificar que la respuesta contiene la estructura esperada
                response_data = post.json()
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    return response_data["choices"][0]["message"]["content"]
                else:
                    # Si la respuesta no contiene la estructura esperada
                    return f"{ERROR_MESSAGE} (Komodo AI-Server {i+1})"

            except requests.exceptions.RequestException as e:
                # En caso de error de red o de conexión con el modelo actual
                print(f"Error de conexión con {model}: {e}")  # Se puede imprimir en el log para depuración
                continue  # Pasar al siguiente modelo

            except (KeyError, ValueError) as e:
                # Si el formato de la respuesta no es el esperado
                print(f"Error en los datos de la respuesta con {model}: {e}")  # Se puede imprimir en el log para depuración
                continue  # Pasar al siguiente modelo

        # Si todos los modelos fallan, el ciclo volverá al primer modelo
        # No se termina, el ciclo sigue indefinidamente

    # Si alguna vez sale del ciclo por alguna razón, retornará el mensaje de error
    return f"{ERROR_MESSAGE} (Komodo AI-Server {i+1})"


def load_memory():
    """Carga la memoria desde el archivo JSON, añadiendo una explicación predeterminada si es necesario"""
    # Crear la carpeta 'datamedia' si no existe
    if not os.path.exists("datamedia"):
        os.makedirs("datamedia")

    # Si el archivo no existe, lo creamos con la explicación predeterminada
    if not os.path.exists(MEMORY_FILE):
        memory = [DEFAULT_MEMORY_EXPLANATION, {"interactions": 0}]
        save_memory(memory)
    else:
        try:
            with open(MEMORY_FILE, "r") as file:
                memory = json.load(file)
        except (json.JSONDecodeError):
            memory = [DEFAULT_MEMORY_EXPLANATION, {"interactions": 0}]
            save_memory(memory)

    return memory


def save_memory(memory):
    """Guarda la memoria en el archivo JSON"""
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def update_memory(user_message, bot_response):
    """Actualiza la memoria con el nuevo mensaje y la respuesta"""
    memory = load_memory()

    # Añadir la nueva interacción a la memoria (solo los últimos mensajes)
    memory.append(f"Usuario: {user_message}")

    # Limitar la longitud de la respuesta del bot
    bot_response_limited = bot_response[:MAX_MESSAGE_LENGTH_BOT]

    # Guardar solo la respuesta limitada
    memory.append(f"Bot: {bot_response_limited}")

    # Incrementar el contador de interacciones
    memory[1]["interactions"] += 1

    # Comprobar si se deben borrar las primeras interacciones
    if memory[1]["interactions"] >= MAX_INTERACTIONS_BEFORE_CLEAN:
        # Borrar las primeras interacciones, pero mantener las últimas
        memory = memory[-MAX_INTERACTIONS_BEFORE_CLEAN:]

        # Reiniciar el contador de interacciones
        memory[1]["interactions"] = 0

    # Guardar de nuevo la memoria en el archivo JSON
    save_memory(memory)


def register(commands):
    commands["bot"] = ai_command  # Puedes cambiar estos prefijos por los que quieras o eliminar los sobrantes.
    commands["ia"] = ai_command
    commands["ai"] = ai_command
