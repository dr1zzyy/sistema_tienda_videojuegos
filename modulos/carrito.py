import os
import json

from modulos import catalogo 
from modulos import calcular
from modulos.os import clean

RUTA = "carrito.json"
MAX_CHARS = 30

# Vacia el carrito
def vaciar():
    with open(RUTA, "w") as carrito:
        json.dump([], carrito)

# Busca un producto en el carrito
def buscar(target=""):

    carrito = catalogo.leer(RUTA) or []

    lista_str = []

    metadatos = {}

    encontrado = False

    for dicc in carrito:
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
            elif clave == "cantidad":
                game += f"| 🛒 x{int(valores)}"
                metadatos["cantidad"] = int(valores)

        if target == "":
            lista_str.append(game)

        if target != "" and ID == target:
            encontrado = True
            lista_str.append(game)
            juego, = lista_str
            return juego, encontrado, metadatos

    if target == "":
        return lista_str if lista_str else ["📭  El carrito está vacío"]

    lista_str.append("❌  Juego no encontrado")
    for md in metadatos:
        metadatos[md] = "...."
    return lista_str, encontrado, metadatos

# Inserta un producto en el carrito
def insertar(ID, metadatos):
    nombre = metadatos["nombre"]
    precio = metadatos["precio"]
    cantidad = metadatos["cantidad"]

    carrito = catalogo.leer(RUTA)

    cantidad_actual = next(
        (juego[ID].get("cantidad", 0) for juego in carrito if ID in juego),
        0
    )
    
    if any(ID in g for g in carrito):
        
        carrito = [g for g in carrito if ID not in g]


        game = {
            ID : {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad+cantidad_actual
            }
        }

    else:
        game = {
            ID : {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad
            }
        }

    carrito.append(game)

    with open(RUTA, "w") as f:
        json.dump(carrito, f, indent=4, ensure_ascii=False)

    catalogo.actualizar({ID:cantidad})

    print("\n✅  Producto agregado al carrito")


# Elimina un producto completo del carrito
def retirar(ID:str):
    if ID == "":
        print("\n⚠️  Ingresa un código válido")
        return False

    juego,encontrado,metadatos = buscar(ID)

    if encontrado == False:
        print("\n🛒 Este juego no esta en tu carrito...")
        return False

    nombre = metadatos["nombre"]

    carrito = catalogo.leer(RUTA)

    if os.path.exists(RUTA) and os.path.getsize(RUTA) > 0:
        try:
            with open(RUTA, "r") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError:
            datos = []
    else:
        datos = []

    INPUT = [u for u in datos if next(iter(u.keys())) != ID]

    if INPUT == datos:
        print("Este juego no esta en el carrito")
        return False

    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(INPUT, f, indent=4, ensure_ascii=False)

    catalogo.actualizar({ID: metadatos["cantidad"]}, tipo="regreso")
    print(f"\n✅  Juego eliminado del carrito: {nombre}")
    return True

# Se encarga de manejar el carrito cuando se quiere agregar un producto
def agregar(ID:str):
    
    if ID == "":
        return print("\n⚠️  Ingresa un código válido")

    juego,encontrado,metadatos = catalogo.mostrar_catalogo(ID)

    if encontrado == False:
        print("\n❌  Juego no encontrado")
    else:

        nombre = metadatos["nombre"]
        precio = metadatos["precio"]
        inventario = metadatos["inventario"]

        while True:
            clean()
            print(juego)

            cantidad = int(input("\n Cantidad a comprar: "))

            if cantidad <= 0:
                clean()
                print("❌️ Ingresa un numero mayor a cero...")
                seleccion = input("\nENTER para reintentar | S para salir: ")

                if seleccion in ["s", "S"]:
                    False
                    return False
                    break
                else:
                    continue

            if catalogo.hay_existencia(ID, cantidad) == False:
                print(f"\n⚠️  No hay suficientes unidades: puedes comprar maximo {inventario}")
                seleccion = input("\nENTER para reintentar | S para salir: ")

                if seleccion in ["s", "S"]:
                    False
                    return False
                    break
                else:
                    continue

            else:
                metadatos.pop("inventario", None)
                metadatos["cantidad"] = cantidad
                insertar(ID, metadatos=metadatos)
                False
                return True
                

# Muestra el carrito completo
def mostrar():

    carrito = catalogo.leer(RUTA) or []

    lista_str = []

    metadatos = {}

    if len(carrito) > 0:
        for dicc in carrito:
            ID = next(iter(dicc))
            datos = dicc[ID]
            game = f"🏷️ {ID} | "
            for clave, valor in datos.items():
                valores = str(valor)

                if clave == "nombre":
                    game += f"🎮️ {valores:<{MAX_CHARS}}"
                    metadatos["nombre"] = valores
                elif clave == "cantidad":
                    game += f"| 🛒 x{int(valores)}"
                    metadatos["cantidad"] = int(valores)
                elif clave == "precio":
                    precio = f"{float(valor):,.2f}"
                    game += f"| 💲 {precio:>10} "
                    metadatos["precio"] = float(valor)
                
            
            lista_str.append(game)

    else:
        return [], metadatos

    return lista_str,metadatos

# Este es el proceso que se sigue al querer finalizar una compra
def finalizar():
    cupon = "GAME50"
    descuento_cupon = 0.0

    ingresar_cupon = input("Ingresar cupon (I) | Continuar sin cupon (C)... ")

    if ingresar_cupon.lower() == "i":
        
        while True:
            validar = input("Ingresa el cupon... ")
            
            if validar == cupon:
                descuento_cupon = 50.0
                clean()
                print("✅️ Descuento aplicado")
                input("\nEnter para continuar con la compra... ")
                False
                break
            else:
                opcion = input("Cupon invalido Reintentar? (R) | Cancelar(c)... ")
                if opcion.lower() == "r":
                    continue
                if opcion.lower() == "c":
                    clean()
                    False
                    break


    if ingresar_cupon.lower() == "c":
        clean()
        descuento_cupon = 0.0

    carrito = catalogo.leer(RUTA)     

    if len(carrito) == 0:
        clean()
        print("🍃 El carrito esta vacio")
        opcion = input("\nEnter para continuar....")
        return False
    montos = {}
    lista_productos = {}

    clean()
    
    for juego in carrito:
        ID = str(next(iter(juego.keys())))
        metadatos = {}
        
        for juegomd in juego.values():
            metadatos["nombre"] = juegomd["nombre"] 
            metadatos["precio"] = juegomd["precio"]
            metadatos["cantidad"] = juegomd["cantidad"] 
        
        subtotal = round(float(metadatos["precio"]) * int(metadatos["cantidad"]), 2)
        montos[metadatos["precio"]] = int(metadatos["cantidad"])

        lista_productos.update({ID: metadatos["cantidad"]})

        cantidad = f"x{metadatos['cantidad']}"
        izquierda = f"{metadatos['nombre']} {cantidad}"
        monto = f"${subtotal:,.2f}"
        relleno = "_" * max(0, MAX_CHARS * 2 - len(izquierda) - len(monto))

        print(f"{izquierda}{relleno}{monto}")

    importe =  calcular.importe(montos)
    total,descuento,impuesto,cuponaplicado = calcular.total(importe, descuento=0.10, impuesto=0.16, valor_cupon=descuento_cupon)

    monto_subtotal = f" ${importe:,.2f}"
    monto_descuento = f" -${descuento:,.2f}"
    monto_cupon = f" -${cuponaplicado:,.2f}"
    monto_impuesto = f" +${impuesto:,.2f}"
    monto_total = f" ${total:,.2f}"

    print(f"\nSubtotal{"_"*max(0, MAX_CHARS * 2 - len("Subtotal") - len(str(monto_subtotal)))}{monto_subtotal}")
    print(f"Descuento{"_"*max(0, MAX_CHARS * 2 - len("Descuento") - len(monto_descuento))}{monto_descuento}")
    if descuento_cupon != 0.0:
        print(f"Cupon{"_"*max(0, MAX_CHARS * 2 - len("Cupon") - len(monto_cupon))}{monto_cupon}")
    print(f"Impuesto{"_"*max(0, MAX_CHARS * 2 - len("Impuesto") - len(monto_impuesto))}{monto_impuesto}")
    print(f"Total{"_"*max(0, MAX_CHARS * 2 - len("Total") - len(monto_total))}{monto_total}\n")

    while True:
        seleccion = input("➜  ¿Finalizar compra? (S) | Cancelar (C): ")

        if seleccion in ["s", "S"]:
            vaciar()
            return True
        if seleccion in ["c", "C"]:
            return False

        print("⚠️  Opción inválida")



    return round(importe)
        
