import psutil
import json
import os
import requests
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path

# Archivos de configuración
SKIN_FILE = "skin.json"
USERNAME_FILE = "username.json"

# Carpeta de versiones skins dentro del launcher
SKINS_DIR = Path("skins_versions")
SKINS_DIR.mkdir(exist_ok=True)

def ram_total_gb():
    return psutil.virtual_memory().total // (1024**3)

# -------------------------
# Gestión de Skins
# -------------------------

def seleccionar_skin(skin_label):
    ruta = filedialog.askopenfilename(filetypes=[("PNG files","*.png")])
    if ruta:
        with open(SKIN_FILE, "w", encoding="utf-8") as f:
            json.dump({"skin": ruta}, f)

        try:
            img = Image.open(ruta).resize((64,64))
            preview = ImageTk.PhotoImage(img)
            skin_label.config(image=preview)
            skin_label.image = preview
        except Exception as e:
            skin_label.config(text=f"Error cargando skin: {e}")

def cargar_skin(skin_label):
    if os.path.exists(SKIN_FILE):
        try:
            with open(SKIN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            ruta = data.get("skin")
            if ruta and os.path.exists(ruta):
                img = Image.open(ruta).resize((64,64))
                preview = ImageTk.PhotoImage(img)
                skin_label.config(image=preview)
                skin_label.image = preview
        except Exception as e:
            skin_label.config(text=f"Error cargando skin: {e}")

def obtener_versiones_skins():
    """
    Devuelve únicamente las versiones en la carpeta 'skins_versions'
    que tengan el sufijo '--skin'.
    """
    if not SKINS_DIR.exists():
        return []
    return [d.name for d in SKINS_DIR.iterdir() if d.is_dir() and d.name.endswith("--skin")]

# -------------------------
# Gestión de Username
# -------------------------

def guardar_username(nombre):
    try:
        with open(USERNAME_FILE, "w", encoding="utf-8") as f:
            json.dump({"username": nombre}, f)
    except Exception as e:
        print(f"Error guardando username: {e}")

def cargar_username():
    if os.path.exists(USERNAME_FILE):
        try:
            with open(USERNAME_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("username")
        except Exception as e:
            print(f"Error cargando username: {e}")
            return None
    return None

# -------------------------
# Actualización desde GitHub
# -------------------------

def actualizar_launcher(status_label=None):
    """
    Descarga los archivos del repositorio GitHub y actualiza el launcher.
    No modifica username.json ni skin.json.
    """
    url = "https://api.github.com/repos/tomachiro/launcher/contents"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            files = resp.json()
            for f in files:
                nombre = f["name"]
                if nombre in [USERNAME_FILE, SKIN_FILE]:
                    continue  # no sobrescribir configuraciones personales
                if f["type"] == "file":
                    download_url = f["download_url"]
                    contenido = requests.get(download_url, timeout=10).content
                    with open(nombre, "wb") as out:
                        out.write(contenido)
            if status_label:
                status_label.config(text="Launcher actualizado desde GitHub")
        else:
            if status_label:
                status_label.config(text=f"Error al actualizar: {resp.status_code}")
    except Exception as e:
        if status_label:
            status_label.config(text=f"Error al actualizar: {e}")
