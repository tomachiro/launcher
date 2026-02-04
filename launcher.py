import tkinter as tk
from tkinter import ttk, simpledialog
import threading
from launcher_core import launch_game
from profiles import cargar_perfiles, guardar_perfiles, obtener_versiones, obtener_ultima_version
from loaders import obtener_modloaders_instalados
from utils import (
    ram_total_gb,
    seleccionar_skin,
    cargar_skin,
    obtener_versiones_skins,
    cargar_username,
    guardar_username,
    actualizar_launcher
)

perfiles = cargar_perfiles()

def jugar():
    perfil_nombre = combo_perfiles.get()
    perfil = perfiles.get(perfil_nombre)
    if not perfil:
        status_label.config(text="Perfil no encontrado")
        return
    username = entry_nombre.get().strip() or "steve"
    guardar_username(username)  # guardar cada vez que se use

    progress["value"] = 0
    status_label.config(text="Iniciando...")
    progress.pack(pady=10)

    threading.Thread(
        target=lambda: launch_game(perfil, username, progress, status_label, root, hide_progress)
    ).start()

def hide_progress():
    progress.pack_forget()
    status_label.config(text="")

def configurar_perfil(perfil_nombre=None):
    if not perfil_nombre:
        perfil_nombre = simpledialog.askstring("Nuevo perfil", "Nombre del perfil:")
        if not perfil_nombre:
            return

    perfil = perfiles.get(perfil_nombre, {
        "version": obtener_ultima_version(),
        "ram": "2G",
        "filters": ["release"]
    })

    config_win = tk.Toplevel(root)
    config_win.title(f"Configurar perfil: {perfil_nombre}")
    config_win.resizable(False, False)

    # Barra de RAM
    tk.Label(config_win, text="RAM asignada (GB):").pack()
    ram_var = tk.IntVar(value=int(perfil.get("ram", "2G").replace("G","")))
    scale_ram = tk.Scale(config_win, from_=1, to=ram_total_gb(), orient="horizontal",
                         variable=ram_var, length=300)
    scale_ram.pack(pady=5)

    # Filtros de versiones
    frame_filtros = tk.LabelFrame(config_win, text="Tipos de versiones")
    frame_filtros.pack(pady=5)

    show_release = tk.BooleanVar(value="release" in perfil.get("filters", []))
    show_snapshot = tk.BooleanVar(value="snapshot" in perfil.get("filters", []))
    show_beta = tk.BooleanVar(value="old_beta" in perfil.get("filters", []))
    show_alpha = tk.BooleanVar(value="old_alpha" in perfil.get("filters", []))
    show_modloader = tk.BooleanVar(value="modloader" in perfil.get("filters", []))
    show_skins = tk.BooleanVar(value="skins" in perfil.get("filters", []))

    def actualizar_lista():
        filtros = []
        if show_release.get(): filtros.append("release")
        if show_snapshot.get(): filtros.append("snapshot")
        if show_beta.get(): filtros.append("old_beta")
        if show_alpha.get(): filtros.append("old_alpha")
        versiones = obtener_versiones(filtros)

        if show_modloader.get():
            versiones += obtener_modloaders_instalados()

        if show_skins.get():
            versiones += obtener_versiones_skins()

        combo_version["values"] = versiones
        if perfil.get("version") in versiones:
            combo_version.set(perfil.get("version"))
        elif versiones:
            combo_version.current(0)

    tk.Checkbutton(frame_filtros, text="Release", variable=show_release, command=actualizar_lista).pack(anchor="w")
    tk.Checkbutton(frame_filtros, text="Snapshots", variable=show_snapshot, command=actualizar_lista).pack(anchor="w")
    tk.Checkbutton(frame_filtros, text="Betas antiguas", variable=show_beta, command=actualizar_lista).pack(anchor="w")
    tk.Checkbutton(frame_filtros, text="Alphas antiguas", variable=show_alpha, command=actualizar_lista).pack(anchor="w")
    tk.Checkbutton(frame_filtros, text="Modloader", variable=show_modloader, command=actualizar_lista).pack(anchor="w")
    tk.Checkbutton(frame_filtros, text="Skins", variable=show_skins, command=actualizar_lista).pack(anchor="w")

    tk.Label(config_win, text="Versión de Minecraft:").pack()
    combo_version = ttk.Combobox(config_win, state="readonly", width=40)
    combo_version.pack(pady=5)
    actualizar_lista()

    def guardar_config():
        filtros = []
        if show_release.get(): filtros.append("release")
        if show_snapshot.get(): filtros.append("snapshot")
        if show_beta.get(): filtros.append("old_beta")
        if show_alpha.get(): filtros.append("old_alpha")
        if show_modloader.get(): filtros.append("modloader")
        if show_skins.get(): filtros.append("skins")

        perfiles[perfil_nombre] = {
            "version": combo_version.get(),
            "ram": f"{ram_var.get()}G",
            "filters": filtros
        }
        guardar_perfiles(perfiles)
        combo_perfiles["values"] = list(perfiles.keys())
        config_win.destroy()

    tk.Button(config_win, text="Guardar", command=guardar_config).pack(pady=5)

# Interfaz principal
root = tk.Tk()
root.title("Launcher de Tomás")
root.geometry("500x550")
root.resizable(False, False)

# Botón de actualizar en esquina superior derecha
btn_actualizar = tk.Button(root, text="Actualizar", command=lambda: actualizar_launcher(status_label))
btn_actualizar.place(x=420, y=10)

tk.Label(root, text="Nombre de usuario:", font=("Arial", 10)).pack()
entry_nombre = tk.Entry(root, width=30)
entry_nombre.pack(pady=5)

# Cargar nombre guardado
nombre_guardado = cargar_username()
if nombre_guardado:
    entry_nombre.insert(0, nombre_guardado)
else:
    entry_nombre.insert(0, "steve")

tk.Label(root, text="Selecciona perfil:", font=("Arial", 12)).pack(pady=10)
combo_perfiles = ttk.Combobox(root, values=list(perfiles.keys()), state="readonly", width=40)
combo_perfiles.pack(pady=5)
if perfiles:
    combo_perfiles.current(0)

btn_jugar = tk.Button(root, text="Jugar Minecraft", command=jugar)
btn_jugar.pack(pady=5)

btn_config = tk.Button(root, text="Configurar perfil", command=lambda: configurar_perfil(combo_perfiles.get()))
btn_config.pack(pady=5)

btn_nuevo = tk.Button(root, text="Nuevo perfil", command=lambda: configurar_perfil(None))
btn_nuevo.pack(pady=5)

# Botón para seleccionar skin global
tk.Label(root, text="Skin global del launcher:").pack(pady=5)
skin_label = tk.Label(root)
skin_label.pack(pady=5)

btn_skin = tk.Button(root, text="Seleccionar skin",
                     command=lambda: seleccionar_skin(skin_label))
btn_skin.pack(pady=5)

# Cargar skin previa si existe
cargar_skin(skin_label)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack_forget()

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

# Guardar username al cerrar ventana
def on_close():
    username = entry_nombre.get().strip() or "steve"
    guardar_username(username)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
