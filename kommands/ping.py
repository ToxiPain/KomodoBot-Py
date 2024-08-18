import time
import psutil  # Para obtener estadísticas del sistema
import platform  # Para obtener la información del sistema operativo
import config  # Importar el archivo de configuración

start_time = time.time()
last_ping_time = start_time

def register(commands):
    commands["ping"] = ping_command

def ping_command(client, message, args):
    global last_ping_time

    try:
        current_time = time.time()
        response_time = (current_time - last_ping_time) * 100  # Tiempo de respuesta en milisegundos
        last_ping_time = current_time
        
        uptime = current_time - start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_formatted = f"{hours}h {minutes}m {seconds}s"
        
        # Obtener el número total de comandos procesados desde config
        commands_processed = config.commands_processed

        # Información del sistema
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_used = memory_info.used / (1024 * 1024)  # Convertir a MB
        memory_total = memory_info.total / (1024 * 1024)  # Convertir a MB

        # Información del sistema operativo
        os_info = platform.system() + " " + platform.release()

        # Mensaje de respuesta incluyendo el conteo de comandos procesados y otras estadísticas
        response_message = (
            f"*╰► Pong!! 🏓*\n\n"
            f"*⿻ Tiempo de Respuesta:* {int(response_time)}ms\n"
            f"*⿻ Tiempo Activo:* {uptime_formatted}\n"
            f"*⿻ Comandos Procesados:* {commands_processed}\n"
            f"*⿻ Uso de CPU:* {cpu_usage}%\n"
            f"*⿻ Memoria Usada:* {memory_used:.2f}MB / {memory_total:.2f}MB\n"
            f"*⿻ Sistema Operativo:* {os_info}\n"
        )
        client.reply_message(response_message, message)
    
    except Exception as e:
        client.reply_message(f"Error: {str(e)}", message)
