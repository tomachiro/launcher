from minecraft_launcher_lib import utils
import os
from pathlib import Path

if os.name == "nt":
    BASE_DIR = Path(os.getenv("APPDATA")) / ".minecraft"
else:
    BASE_DIR = Path.home() / ".minecraft"

def obtener_modloaders_instalados():
    versions_dir = BASE_DIR / "versions"
    if not versions_dir.exists():
        return []

    # Lista oficial de Mojang
    vanilla_versions = [v["id"] for v in utils.get_version_list()]

    # Carpeta local
    local_versions = [d.name for d in versions_dir.iterdir() if d.is_dir()]

    # Solo devolver las que NO están en vanilla → modloaders
    return [v for v in local_versions if v not in vanilla_versions]
