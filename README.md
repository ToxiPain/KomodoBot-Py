> NOTA: HAY FUNCIONES QUE AÚN SIGUEN EN FASE DE PRUEBA, CUALQUIER ERROR FAVOR REPORTARLO

# KomodoBot-Python MEJORAS Y TESTEO (BETA) 🌅 --- BUILD 1
**Base-Bot Simple de Whatsapp hecho en Python utilizando <a href="https://github.com/ToxiPain/snakechat">Mod: Snakechat API</a>.** 
KomodoBot-Python es un Bot simple, optimizado y sencillo de editar. Disponible para editarse de forma facil para crear un bot funcional y útil en poco tiempo y sin esfuerzos.

## Info. Oficial:
**-Contactanos:**

<a href="http://wa.me/50557418454" target="blank"><img src="https://img.shields.io/badge/ToxiPain-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />
<a href="http://wa.me/50585424403" target="blank"><img src="https://img.shields.io/badge/Démogo-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />

**-Anuncios y Actualizaciones:**

[![blog](https://img.shields.io/badge/Canal-actulizaciones-25D366?style=for-the-badge&logo=whatsapp&logoColor=white 
)](https://whatsapp.com/channel/0029VaeaBGb2UPB80GbJ420a)  <a href="https://whatsapp.com/channel/0029VaeaBGb2UPB80GbJ420a"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/WhatsApp_logo-color-vertical.svg/1200px-WhatsApp_logo-color-vertical.svg.png" height="29px">
</a>

## Funcionalidades:
Actualmente contamos con las siguientes funcionalidades:

* **Definir distintos envios de mensajes de texto**
* **Comando IA personalizable**
* **Envio de Imagenes personalizadas**
* **Envio de Botones Interactivos**
* **En futuras versiones se añadirán mas funciones...**

## Instalación:
Estas son los metodos de instalación disponibles actualmente:

### `▢ Uso en Termux >_`
> Primero debes descargar el repositorio, arriba a la derecha en la parte de "Code" dar a Download ZIP y una vez descargado extraer la carpeta dentro de descargas.

1. Descargar Termux: https://f-droid.org/packages/com.termux/
<h4></h4>
<pre>
<p># Instalación en Termux</p>
termux-setup-storage
cd storage/downloads/KomodoBot-Py-master/KomodoBot-Py-master
pkg update && pkg upgrade -y
pkg install python3

pkg install libjpeg-turbo
LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow

pip install python-magic
pip install -r requirements.txt
python index.py
</pre>

> Reconectar en Termux: cd storage/downloads/KomodoBot-Py-master/KomodoBot-Py-master && python index.py
   
### `▢ Activar en Replit 🔶`
Activa el Bot desde la plataforma de Replit: 

[![Run on Repl.it](https://repl.it/badge/github/ToxiPain/KomodoBot-Py)](https://repl.it/github/ToxiPain/KomodoBot-Py)

### `▢ Instalar en Windows 🖥️`
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/ToxiPain/KomodoBot-Py.git
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Iniciar el Bot:
   ```bash
   py index.py
   ```

### `▢ Instalalo en Nuestro Host Privado Activo 24/7 (PROXIMAMENTE)`

## Errores Frecuentes:
*En caso de saltar el error de "Libmagic" en windows usar:*
> pip uninstall python-magic

Darle a "Y" y luego

> pip install python-magic-bin==0.4.14

Esto debería solucionar ese error.

PROXIMAMENTE SERÁN AÑADIDAS NUEVAS FUNCIONES BASES.
