from datetime import datetime
import re
from utils_colores import Colores


class Contacto:

    def __init__(self, nombre, correo, telefono, activo=True, fecha_creacion=None):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.activo = activo
        self.fecha_creacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d")

    # -------------------------
    # MOSTRAR INFORMACIÓN
    # -------------------------
    def mostrar_info(self):
        estado = "🟢 Activo" if self.activo else "🔴 Inactivo"
        print(Colores.texto(Colores.CYAN, f"👤 Nombre: {self.nombre}"))
        print(f"📧 Correo: {self.correo}")
        print(f"📞 Teléfono: {self.telefono}")
        print(f"📅 Fecha creación: {self.fecha_creacion}")
        print(f"📌 Estado: {estado}")

    # -------------------------
    # SERIALIZACIÓN
    # -------------------------
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("nombre"),
            data.get("correo"),
            data.get("telefono"),
            data.get("activo", True),
            data.get("fecha_creacion")
        )

    # -------------------------
    # VALIDACIONES
    # -------------------------
    @staticmethod
    def validar_correo(correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, correo) is not None

    @staticmethod
    def validar_telefono(telefono):
        return telefono.isdigit() and len(telefono) == 10
