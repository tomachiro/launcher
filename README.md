Launcher de Tomás
=================

Un launcher personalizado para Minecraft, escrito en Python, con soporte para perfiles, skins globales y actualizaciones automáticas desde GitHub.
Este proyecto busca ofrecer una experiencia clara, flexible y adaptable para cualquier usuario que quiera gestionar sus versiones de Minecraft con facilidad.

Características
---------------
- Perfiles personalizados:
  Cada perfil guarda versión, RAM asignada y filtros de versiones (release, snapshot, beta, alpha, modloader, skins).

- Gestión de skins globales (en proceso):
  Actualmente el sistema de skins está en desarrollo.
  Se pueden seleccionar archivos PNG y mostrarlos en la interfaz, pero la integración completa con mods como CustomSkinLoader y OpenMCSkins está en progreso.

- Persistencia de usuario:
  El nombre de usuario se guarda automáticamente en "username.json" y se carga al iniciar el launcher.

- Actualización automática:
  Botón “Actualizar” que descarga los archivos del repositorio GitHub sin sobrescribir configuraciones personales ("username.json" y "skin.json").

- Verificación de Java:
  Al iniciar, el launcher comprueba si Java está instalado y muestra una alerta si no lo está.

Requisitos
----------
- Java (JRE/JDK) instalado en el sistema (necesario para ejecutar Minecraft).
- Librerías de Python (solo necesarias para desarrollo, no para usuarios finales):
  psutil, requests, pillow

Uso
---
1. Clona el repositorio:
   git clone https://github.com/tomachiro/launcher.git
   cd launcher

2. Ejecuta el launcher:
   python launcher.py

3. Configura tu perfil, selecciona tu skin y juega.

Notas
-----
- Las versiones con soporte de skins deben colocarse en la carpeta "skins_versions/" y llevar el sufijo "--skin".
- El botón “Actualizar” descarga los archivos del repositorio y mantiene tus configuraciones personales.
- El sistema de skins está en proceso de desarrollo y se irá ampliando en futuras versiones.
- Si Java no está instalado, el launcher mostrará una alerta con el enlace oficial de descarga.

Participación
-------------
Este proyecto cuenta con la asistencia de Copilot (Microsoft AI), colaborando en la optimización del flujo, modularización del código, persistencia de configuraciones y diseño del sistema de skins.

Propósito
---------
Este proyecto es únicamente experimental y educativo, creado para:
- Estudiar el razonamiento de Copilot en proyectos de este estilo.
- Experimentar la combinación de librerías de Python con un juego como Minecraft Java.

No está pensado para distribución comercial ni para reemplazar el launcher oficial de Minecraft.
