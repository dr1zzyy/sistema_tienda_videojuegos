import os

#Limpiar terminal
def clean():
    os.system("cls" if os.name == "nt" else "clear")