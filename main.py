from operaciones import GestorContactos
from utils_colores import Colores, clear

def main():
    gestor = GestorContactos()

    while True:
        print(Colores.texto(Colores.AZUL, "\n=== 📇 GESTOR DE CONTACTOS ==="))
        print("1️⃣  Agregar contacto")
        print("2️⃣  Listar contactos")
        print("3️⃣  Buscar contacto")
        print("4️⃣  Editar contacto")
        print("5️⃣  Eliminar contactos")
        print("6️⃣  Ordenar contactos")
        print("7️⃣  Cambiar estado activo/inactivo")
        print("8️⃣  Exportar contactos a CSV")
        print("9️⃣  Salir")

        opcion = input("👉 Seleccione una opción: ")

        if opcion == "1":
            clear()
            gestor.agregar_contacto()
        elif opcion == "2":
            clear()
            gestor.listar_contactos()
        elif opcion == "3":
            clear()
            gestor.buscar_contacto()
        elif opcion == "4":
            clear()
            gestor.editar_contacto()
        elif opcion == "5":
            clear()
            gestor.eliminar_multiple()
        elif opcion == "6":
            clear()
            gestor.ordenar_contactos()
        elif opcion == "7":
            clear()
            gestor.cambiar_estado()
        elif opcion == "8":
            clear()
            gestor.exportar_csv()
        elif opcion == "9":
            print(Colores.texto(Colores.VERDE, "👋 Saliendo..."))
            break
        else:
            print(Colores.texto(Colores.ROJO, "❌ Opción no válida"))

        input(Colores.texto(Colores.CYAN, "\nPresione Enter para continuar..."))

if __name__ == "__main__":
    main()
