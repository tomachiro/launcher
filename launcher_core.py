import os
import subprocess
from pathlib import Path
from minecraft_launcher_lib import install, command

# Carpeta oficial de Minecraft
if os.name == "nt":
    BASE_DIR = Path(os.getenv("APPDATA")) / ".minecraft"
else:
    BASE_DIR = Path.home() / ".minecraft"

def launch_game(perfil, username, progress=None, status_label=None, root=None, hide_progress=None):
    try:
        version_id = perfil.get("version")
        ram = perfil.get("ram", "2G")
        loader_version = perfil.get("loader_version", "")

        if status_label: status_label.config(text=f"Verificando {version_id}...")
        install.install_minecraft_version(version_id, str(BASE_DIR))

        if progress: progress["value"] = 70
        if root: root.update_idletasks()

        options = {
            "username": username,
            "uuid": "00000000-0000-0000-0000-000000000000",
            "token": "0"
        }

        # Si el perfil tiene un modloader instalado, usar esa versión
        version_to_launch = loader_version if loader_version else version_id
        cmd = command.get_minecraft_command(version_to_launch, str(BASE_DIR), options)
        cmd.insert(1, f"-Xmx{ram}")

        if progress: progress["value"] = 100
        if status_label: status_label.config(text="Ejecutando Minecraft...")
        if root: root.update_idletasks()

        subprocess.run(cmd)

        if hide_progress:
            hide_progress()

    except Exception as e:
        if status_label: status_label.config(text=f"Error: {e}")
        if hide_progress:
            hide_progress()
