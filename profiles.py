import os
import json
from minecraft_launcher_lib import utils

PROFILES_FILE = "profiles.json"

def obtener_ultima_version():
    manifest = utils.get_version_list()
    for v in manifest:
        if v["type"] == "release":
            return v["id"]
    return manifest[0]["id"]

def cargar_perfiles():
    if not os.path.exists(PROFILES_FILE):
        perfiles = {
            "lasted": {
                "version": obtener_ultima_version(),
                "ram": "2G",
                "filters": ["release"],
                "loader_version": ""
            }
        }
        guardar_perfiles(perfiles)
        return perfiles
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_perfiles(perfiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(perfiles, f, indent=4)

def obtener_versiones(filtros=None):
    manifest = utils.get_version_list()
    if filtros:
        return [v["id"] for v in manifest if v["type"] in filtros]
    else:
        return [v["id"] for v in manifest]
