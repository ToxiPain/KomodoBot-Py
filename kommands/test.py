from PIL import Image, ImageDraw, ImageFont
import random
import io

def generate_image_with_text(text):
    """Genera una imagen con texto usando Pillow."""
    width, height = 512, 512  # Tamaño de sticker
    image = Image.new('RGBA', (width, height), color=random_color())
    draw = ImageDraw.Draw(image)
    font_size = random.randint(20, 50)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Usa una fuente TrueType
    except IOError:
        font = ImageFont.load_default()  # Fuente predeterminada si arial.ttf no está disponible

    # Usar textbbox para calcular el tamaño del texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    draw.text((text_x, text_y), text, font=font, fill=random_color())
    image = image.convert('RGB')  # Convertir a RGB antes de guardar como WebP
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='WEBP')
    image_bytes.seek(0)

    return image_bytes

def random_color():
    """Genera un color aleatorio en formato RGB."""
    return tuple(random.randint(0, 255) for _ in range(3))

def register(commands):
    """Registra el comando !sticker."""
    def sticker_command(client, message, args):
        if args:
            text = ' '.join(args)
            image_bytes = generate_image_with_text(text)
            # Enviar el sticker
            client.send_sticker(
                message.Info.MessageSource.Chat,
                image_bytes,
                name="@Neonize",
                packname="2024"
            )
        else:
            client.reply_message("Por favor, proporciona el texto para el sticker.", message)

    commands['sticker'] = sticker_command
