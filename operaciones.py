import json
import os
import csv
from contacto import Contacto
from utils_colores import Colores

# ------------------------
# ARCHIVO JSON
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE_DIR, "contactos.json")

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    os.makedirs(os.path.dirname(ARCHIVO), exist_ok=True)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write("[]")

# ------------------------
# CLASE GESTOR CONTACTOS
# ------------------------
class GestorContactos:
    def __init__(self, archivo=ARCHIVO):
        self.archivo = archivo
        self.contactos = []
        self.cargar_contactos()

    def cargar_contactos(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    self.contactos.append(Contacto.from_dict(item))
        except Exception:
            self.contactos = []

    def guardar_contactos(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.contactos], f, indent=4, ensure_ascii=False)

    # ------------------------
    # AGREGAR CONTACTO
    # ------------------------
    def agregar_contacto(self):
        print(Colores.texto(Colores.AZUL, "\n➕ NUEVO CONTACTO"))
        nombre = input("👤 Nombre: ").strip().title()
        correo = input("📧 Correo: ").strip().lower()
        telefono = input("📞 Teléfono (10 dígitos): ").strip()

        if not Contacto.validar_correo(correo):
            print(Colores.texto(Colores.ROJO, "❌ Correo inválido"))
            return

        if not Contacto.validar_telefono(telefono):
            print(Colores.texto(Colores.ROJO, "❌ Teléfono inválido"))
            return

        if any(c.correo == correo for c in self.contactos):
            print(Colores.texto(Colores.AMARILLO, "⚠️ Contacto duplicado"))
            return

        self.contactos.append(Contacto(nombre, correo, telefono))
        self.guardar_contactos()
        print(Colores.texto(Colores.VERDE, "✅ Contacto agregado correctamente"))

    # ------------------------
    # ORDENAR CONTACTOS
    # ------------------------

    def ordenar_contactos(self):
        if not self.contactos:
            print(Colores.texto(
                Colores.AMARILLO,
                "📭 No hay contactos para ordenar."
            ))
            return

        print(Colores.texto(Colores.CYAN, "\n📊 ORDENAR CONTACTOS"))
        print("1️⃣ Nombre (A–Z)")
        print("2️⃣ Fecha de creación (más recientes)")
        print("3️⃣ Fecha de creación (más antiguos)")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            self.contactos.sort(key=lambda c: c.nombre)
            print(Colores.texto(
                Colores.VERDE,
                "✅ Contactos ordenados alfabéticamente."
            ))

        elif opcion == "2":
            self.contactos.sort(key=lambda c: c.fecha_creacion, reverse=True)
            print(Colores.texto(
                Colores.VERDE,
                "✅ Contactos ordenados por más recientes."
            ))

        elif opcion == "3":
            self.contactos.sort(key=lambda c: c.fecha_creacion)
            print(Colores.texto(
                Colores.VERDE,
                "✅ Contactos ordenados por más antiguos."
            ))

        else:
            print(Colores.texto(
                Colores.AMARILLO,
                "⚠️ Opción no válida."
            ))
            return

        self.listar_contactos()


    # ------------------------
    # LISTAR CONTACTOS
    # ------------------------
    def listar_contactos(self):
        if not self.contactos:
            print(Colores.texto(Colores.AMARILLO, "📭 No hay contactos"))
            return
        print(Colores.texto(Colores.AZUL, "\n📋 LISTA DE CONTACTOS"))
        for i, c in enumerate(self.contactos, start=1):
            print(Colores.texto(Colores.MAGENTA, f"\n#{i}"))
            c.mostrar_info()

    # ------------------------
    # BUSCAR CONTACTO
    # ------------------------
    def buscar_contacto(self):
        termino = input("🔎 Buscar por nombre o correo: ").lower()
        resultados = [c for c in self.contactos if termino in c.nombre.lower() or termino in c.correo.lower()]
        if not resultados:
            print(Colores.texto(Colores.ROJO, "❌ No se encontraron resultados"))
            return
        print(Colores.texto(Colores.VERDE, f"✅ {len(resultados)} resultado(s):"))
        for c in resultados:
            c.mostrar_info()

    # ------------------------
    # CAMBIAR ESTADO
    # ------------------------
    def cambiar_estado(self):
        self.listar_contactos()
        if not self.contactos:
            return
        try:
            idx = int(input("🔄 Número de contacto a cambiar estado: ")) - 1
            contacto = self.contactos[idx]
        except Exception:
            print("❌ Selección inválida")
            return
        contacto.activo = not contacto.activo
        estado = "Activo" if contacto.activo else "Inactivo"
        self.guardar_contactos()
        print(f"✅ Estado cambiado a {estado} para {contacto.nombre}")


    # ------------------------
    # EDITAR CONTACTO
    # ------------------------
    def editar_contacto(self):
        self.listar_contactos()
        if not self.contactos:
            return
        try:
            idx = int(input("✏️ Número a editar: ")) - 1
            contacto = self.contactos[idx]
        except Exception:
            print(Colores.texto(Colores.ROJO, "❌ Selección inválida"))
            return

        print(Colores.texto(Colores.AZUL, "↩️ Enter para mantener valor"))
        nuevo_nombre = input(f"Nombre ({contacto.nombre}): ").strip()
        nuevo_correo = input(f"Correo ({contacto.correo}): ").strip()
        nuevo_tel = input(f"Teléfono ({contacto.telefono}): ").strip()

        if nuevo_nombre:
            contacto.nombre = nuevo_nombre.title()
        if nuevo_correo and Contacto.validar_correo(nuevo_correo):
            contacto.correo = nuevo_correo.lower()
        if nuevo_tel and Contacto.validar_telefono(nuevo_tel):
            contacto.telefono = nuevo_tel

        self.guardar_contactos()
        print(Colores.texto(Colores.VERDE, "✅ Contacto actualizado"))

    # ------------------------
    # ELIMINAR MÚLTIPLE
    # ------------------------
    def eliminar_multiple(self):
        self.listar_contactos()
        if not self.contactos:
            return
        seleccion = input("🗑️ Números a eliminar (1,3,5): ")
        try:
            indices = sorted({int(i.strip()) - 1 for i in seleccion.split(",")}, reverse=True)
            for i in indices:
                if 0 <= i < len(self.contactos):
                    eliminado = self.contactos.pop(i)
                    print(Colores.texto(Colores.ROJO, f"🗑️ Eliminado: {eliminado.nombre}"))
            self.guardar_contactos()
            print(Colores.texto(Colores.VERDE, "✅ Eliminación completada"))
        except Exception:
            print(Colores.texto(Colores.ROJO, "❌ Entrada inválida"))

    # ------------------------
    # CAMBIAR ESTADO
    # ------------------------
    def cambiar_estado(self):
        self.listar_contactos()
        if not self.contactos:
            return
        try:
            idx = int(input("🔄 Número de contacto a cambiar estado: ")) - 1
            contacto = self.contactos[idx]
        except Exception:
            print("❌ Selección inválida")
            return
        contacto.activo = not contacto.activo
        estado = "Activo" if contacto.activo else "Inactivo"
        self.guardar_contactos()
        print(f"✅ Estado cambiado a {estado} para {contacto.nombre}")

    # ------------------------
    # EXPORTAR CSV
    # ------------------------
    def exportar_csv(self):
        if not self.contactos:
            print(Colores.texto(Colores.AMARILLO, "📭 No hay contactos"))
            return
        archivo_csv = os.path.join(BASE_DIR, "contactos_exportados.csv")
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Nombre", "Correo", "Teléfono", "Estado", "Fecha"])
            for c in self.contactos:
                writer.writerow([c.nombre, c.correo, c.telefono, "Activo" if c.activo else "Inactivo", c.fecha_creacion])
        print(Colores.texto(Colores.VERDE, f"📤 Exportado correctamente → contactos_exportados.csv"))
