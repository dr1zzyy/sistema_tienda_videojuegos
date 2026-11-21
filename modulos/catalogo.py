import json
import os

RUTA = "catalogo.json"

MAX_CHARS = 30

# Leer el archivo de catalogo
def leer(ruta):
    if os.path.exists(ruta) and os.path.getsize(ruta) > 0:
        with open(ruta, "r") as catalogo:
                return json.load(catalogo)

# Muestra el producto mas vendido y cuanto se vendio
def mas_vendido():
    catalogo = leer(RUTA)
    lista = {}

    for game in catalogo:
        ID = next(iter(game.keys()))
        nombre = next(iter(game.values()))["nombre"]
        ventas = next(iter(game.values()))["vendidos"]
        lista[ID] = {"nombre":nombre, "vendidos":ventas}

    IDM, metadatos = max(lista.items(), key=lambda par: par[1]["vendidos"])

    return IDM, metadatos

    # en caso de querer mostrar todos los juegos y sus ventas
    #for juego in lista.keys():
            #ID = juego
            #datos = lista[ID]
            #nombre,vendidos = datos["nombre"],datos["vendidos"]
            #print(f"🏷️  {ID} {nombre} {vendidos}")
            #print(f"{ID} - {nombre} -> {vendidos}")
        
# Revisa si hay existencia de un producto, y cuanto se requiere de ese producto
def hay_existencia(ID:str, requerido:int=1):

    catalogo = leer(RUTA) or []

    for juego in catalogo:
        if ID in juego:
            inventario = int(juego[ID].get("inventario", 0))
            return requerido <= inventario

    return False

# Funciona tambien como buscar_producto si se le ingresa un ID en target
def mostrar_catalogo(target=""):

    catalogo = leer(RUTA)

    lista_str = []

    metadatos = {}

    encontrado = False

    if len(catalogo) > 0:
        for dicc in catalogo:
            ID = next(iter(dicc))
            datos = dicc[ID]
            game = f"🏷️ {ID} | "
            for clave, valor in datos.items():
                valores = str(valor)

                if clave == "nombre":
                    game += f"🎮️ {valores:<{MAX_CHARS}}"
                    metadatos["nombre"] = valores
                elif clave == "precio":
                    precio = f"{float(valor):,.2f}"
                    game += f"| 💲 {precio:>10} "
                    metadatos["precio"] = float(valor)
                elif clave == "inventario":
                    game += f"| 📦️ {int(valores)}"
                    metadatos["inventario"] = int(valores)
                
            if target == "":
                lista_str.append(game)

            if target != "" and ID == target:
                encontrado = True
                lista_str.append(game)
                juego, = lista_str
                return juego,encontrado,metadatos



    else:
        return ["📭  El catálogo está vacío"]

    if target != "" and encontrado == False:
        lista_str.append("❌  Juego no encontrado")
        for md in metadatos:
            metadatos[md] = "...."
        return lista_str,None, metadatos

    return lista_str

# Actualizar el inventario de un producto, aumenta o reduce la existencia
                                        # (ingreso) (egreso) del inventario
def actualizar(metadatos, tipo="egreso"):
    catalogo = leer(RUTA)

    for juego in catalogo:
        for id_producto, datos in juego.items():
            if id_producto in metadatos:
                if tipo == "egreso":
                    datos["inventario"] = datos["inventario"]-metadatos[id_producto]
                    datos["vendidos"] = datos.get("vendidos", 0)+metadatos[id_producto]
                elif tipo == "regreso":
                    datos["inventario"] = datos["inventario"]+metadatos[id_producto]
                    datos["vendidos"] = datos.get("vendidos", 0)-metadatos[id_producto]
    guardar(catalogo, RUTA)
    return catalogo

# Guardar un archivo json
def guardar(catalogo, ruta=RUTA):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(catalogo, f, indent=4, ensure_ascii=False)



