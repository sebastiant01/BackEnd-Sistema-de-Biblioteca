"""
Operaciones CRUD para Libro
"""

from typing import List, Optional
from uuid import UUID

from entities.Libro import Libro
from sqlalchemy.orm import Session


class LibroCRUD:
    def __init__(self, database: Session):
        self.database = database

    def crear_libro(self):
        pass

    def obtener_libro(self):
        pass

    def obtener_libros(self):
        pass

    def obtener_libro_por_titulo(self):
        pass

    def actualizar_producto(self):
        pass

    def eliminar_producto(self):
        pass
