from modulos.os import clean 

import modulos.catalogo as catalogo
import modulos.carrito as carrito

def mostrar_menu():
    print("🎮  TIENDA DE JUEGOS")
    print("─" * 32)
    print("  1. Ver catálogo")
    print("  2. Buscar por ID")
    print("  3. Ver carrito")
    print("  4. Agregar al carrito")
    print("  5. Quitar del carrito")
    print("  6. Finalizar compra")
    print("  7. Mas vendido")
    print("  (SALIR). Salir")
    print("─" * 32)


def main():
    while True:

        clean()

        mostrar_menu()

        seleccion = input("➜  Opción: ")

        if seleccion == "1":
            clean()
            catalogo_completo = catalogo.mostrar_catalogo()

            print("🛍️  CATÁLOGO DE JUEGOS")
            print("─" * 48, end="\n\n")

            for juego in catalogo_completo:
                print(juego)

            input("\nEnter para continuar...")

        if seleccion == "2":
            clean()
            ID = input("➜  ID a buscar: ")
            juego,encontrado,metadatos = catalogo.mostrar_catalogo(ID)
            if encontrado:
                print("\n"+juego)
            else:
                print("\n❌  Juego no encontrado")
            input("\nEnter para continuar...")

        if seleccion == "3":
            clean()
            carrito_completo,metadatos = carrito.mostrar()

            print("🛒  TU CARRITO")
            print("─" * 48, end="\n\n")

            if len(carrito_completo) == 0:
                print("🍃  El carrito está vacío")
            else:
                for juego in carrito_completo:
                    print(juego)
                    
            input("\nEnter para continuar...")

        if seleccion == "4":
            clean()

            ID = input("➜  ID del juego: ")

            agregar = carrito.agregar(ID)

            if agregar is False:
                print("\n❌  No se pudo agregar el producto")
                

            input("\nEnter para continuar...")

        if seleccion == "5":
            clean()
            ID = input("Ingresa el id del juego... ")
            eliminar = carrito.retirar(ID)

            clean()

            if eliminar:
                print("\n🪰⠀Has eliminado el juego correctamente de tu carrito...")
                print("─" * 48, end="\n\n")
            else:
                print("❌️ Hubo un error... ")
                print("─" * 48, end="\n\n")

            input("\nEnter para continuar...")

        if seleccion == "6":
            clean()
            print("🧾  RESUMEN DE LA COMPRA")
            print("─" * 60, end="\n\n")
            finalizar = carrito.finalizar()

            if finalizar:
                clean()
                print("✅  Compra finalizada")
                print("🛒  Carrito vaciado")
                print("📦  Inventario actualizado")
            else:
                clean()
                print("⚠️  La compra no se finalizó")

            input("\nEnter para continuar...")

        if seleccion == "7":
            clean()
            ID, md = catalogo.mas_vendido();
            print(f"+ {md["vendidos"]} VENTAS❗️")
            print("─" * 48, end="\n\n")
            juego,encontrado,metadatos = catalogo.mostrar_catalogo(ID)

            print(juego)
            
            input("\nEnter para continuar...")

        if seleccion.lower() == "salir":
            clean()
            print("Gracias por usar el sistema")
            False
            break

main()