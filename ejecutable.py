from cx_Freeze import setup, Executable

setup(
    name="Launcher de Tomás",
    version="1.0",
    description="Launcher experimental para Minecraft",
    executables=[
        Executable("launcher.py", base="gui")
    ]
)
