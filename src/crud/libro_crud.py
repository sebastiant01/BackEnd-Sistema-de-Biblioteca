"""
Operaciones CRUD para Libro

Gestiona la creación, lectura, actualización y eliminación de libros,
teniendo en cuenta la herencia por tabla unida con MaterialBiblioteca.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy.orm import Session

from src.entities.Libro import Libro


class LibroCRUD:
    def __init__(self, database: Session):
        self.database = database

    def crear_libro(
        self,
        codigo_libro: str,
        titulo_libro: str,
        genero_libro: str,
        id_autor: UUID,
        codigo_isbn: str,
        id_usuario_crea: UUID,
        descripcion_libro: Optional[str] = None,
        fecha_libro: Optional[date] = None,
        disponibilidad: bool = True,
    ):
        """
        Crea un nuevo libro en la base de datos.

        Inserta automáticamente en materiales_biblioteca y libros
        gracias a la herencia por tabla unida. tipo_material se
        asigna automáticamente como TipoMaterial.libro.

        Args:
            codigo_material:         Código interno único del material.
            titulo_material:         Título del libro.
            id_autor:                UUID del autor principal del libro.
            codigo_isbn:             Código ISBN único del libro.
            genero_libro:            Género literario del libro.
            id_usuario_crea:         UUID del usuario que registra el libro.
            disponibilidad_material: Disponibilidad inicial (True por defecto).
            descripcion_material:    Descripción opcional del libro.
            fecha_material:          Fecha de publicación del libro.

        Returns:
            Libro: Instancia del libro recién creado.

        Raises:
            ValueError: Si algún campo obligatorio es inválido o ya existe.
        """

        if not codigo_libro or len(codigo_libro.strip()) == 0 or codigo_libro[0] != "L":
            raise ValueError(
                "El código del libro es obligatorio, y debe de empezar con L"
            )

        if not titulo_libro or len(titulo_libro.strip()) == 0:
            raise ValueError("El título del material es obligatorio")

        if not codigo_isbn or len(codigo_isbn.strip()) == 0:
            raise ValueError("El código ISBN es obligatorio")

        if not genero_libro or len(genero_libro.strip()) == 0:
            raise ValueError("El género del libro es obligatorio")

        if not id_autor:
            raise ValueError("El ID del autor correspondiente es obligatorio")

        if not id_usuario_crea:
            raise ValueError("El ID del usuario que lo creó es obligatorio")

        existente_isbn = (
            self.database.query(Libro)
            .filter(Libro.codigo_isbn == codigo_isbn.strip())
            .first()
        )

        if existente_isbn:
            raise ValueError(f"Ya existe un libro con este código ISBN: {codigo_isbn}")

        existente_codigo = (
            self.database.query(Libro)
            .filter(Libro.codigo_material == codigo_libro.strip())
            .first()
        )

        if existente_codigo:
            raise ValueError(f"Ya existe un libro con este código: {codigo_libro}")

        nuevo_libro = Libro(
            codigo_material=codigo_libro.strip(),
            titulo_material=titulo_libro.strip(),
            id_autor=id_autor,
            codigo_isbn=codigo_isbn.strip(),
            genero_libro=genero_libro.strip(),
            id_usuario_crea=id_usuario_crea,
            disponibilidad_material=disponibilidad,
            descripcion_material=descripcion_libro,
            fecha_material=fecha_libro,
        )

        self.database.add(nuevo_libro)
        self.database.commit()
        self.database.refresh(nuevo_libro)
        return nuevo_libro

    def obtener_libro(self, id_libro: UUID) -> Optional[Libro]:
        """
        Obtiene un libro por su UUID.

        Realiza automáticamente el JOIN entre materiales_biblioteca y libros.

        Args:
            id_libro: UUID del libro a buscar.

        Returns:
            Libro encontrado o None si no existe.
        """
        return self.database.query(Libro).filter(Libro.id_libro == id_libro).first()

    def obtener_libro_codigo(self, codigo_libro: str) -> Optional[Libro]:
        """
        Obtiene un libro por su código.

        Args:
            codigo_libro: Código del libro a buscar (no confundir con id).

        Returns:
            Libro encontrado o None si no existe.
        """
        return (
            self.database.query(Libro)
            .filter(Libro.codigo_material == codigo_libro)
            .first()
        )

    def obtener_libros(self, skip: int = 0, limit: int = 100) -> List[Libro]:
        """
        Obtiene una lista paginada de todos los libros.

        Args:
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de libros.
        """
        return self.database.query(Libro).offset(skip).limit(limit).all()

    def obtener_libros_por_autor(self, id_autor: UUID) -> List[Libro]:
        """
        Obtiene todos los libros de un autor específico.

        Args:
            id_autor: UUID del autor.

        Returns:
            Lista de libros del autor.
        """
        return self.database.query(Libro).filter(Libro.id_autor == id_autor).all()

    def obtener_libros_disponibles(self) -> List[Libro]:
        """
        Obtiene todos los libros con disponibilidad_material en True.

        Returns:
            Lista de libros disponibles para préstamo.
        """
        return (
            self.database.query(Libro)
            .filter(Libro.disponibilidad_material == True)
            .all()
        )

    def buscar_libros_por_titulo(self, titulo: str) -> List[Libro]:
        """
        Busca libros por título (búsqueda parcial, sin distinguir mayúsculas).

        Args:
            titulo: Texto a buscar en el título.

        Returns:
            Lista de libros que coinciden con el título.
        """
        return (
            self.database.query(Libro)
            .filter(Libro.titulo_material.ilike(f"%{titulo}%"))
            .all()
        )

    def buscar_libros_por_genero(self, genero: str) -> List[Libro]:
        """
        Busca libros por género literario (búsqueda parcial).

        Args:
            genero: Género a buscar.

        Returns:
            Lista de libros que coinciden con el género.
        """
        return (
            self.database.query(Libro)
            .filter(Libro.genero_libro.ilike(f"%{genero}%"))
            .all()
        )

    def actualizar_libro(
        self,
        id_libro: UUID,
        id_usuario_edita: UUID,
        **kwargs,
    ) -> Optional[Libro]:
        """
        Actualiza los campos de un libro existente.

        Permite actualizar tanto campos de Libro como de MaterialBiblioteca.
        id_usuario_edita es obligatorio para mantener la trazabilidad de auditoría.

        Args:
            id_libro:         UUID del libro a actualizar.
            id_usuario_edita: UUID del usuario que realiza la modificación.
            **kwargs:         Campos a actualizar (titulo_material, genero_libro, etc.).

        Returns:
            Libro actualizado o None si no existe.

        Raises:
            ValueError: Si algún campo tiene un valor inválido.
        """
        libro = self.obtener_libro(id_libro)
        if not libro:
            return None

        if "titulo_material" in kwargs:
            if (
                not kwargs["titulo_material"]
                or len(kwargs["titulo_material"].strip()) == 0
            ):
                raise ValueError("El título no puede estar vacío")
            kwargs["titulo_material"] = kwargs["titulo_material"].strip()

        if "codigo_isbn" in kwargs:
            nuevo_isbn = kwargs["codigo_isbn"].strip()
            existente = (
                self.database.query(Libro)
                .filter(Libro.codigo_isbn == nuevo_isbn, Libro.id_libro != id_libro)
                .first()
            )
            if existente:
                raise ValueError(f"Ya existe un libro con el ISBN '{nuevo_isbn}'")
            kwargs["codigo_isbn"] = nuevo_isbn

        if "genero_libro" in kwargs:
            if not kwargs["genero_libro"] or len(kwargs["genero_libro"].strip()) == 0:
                raise ValueError("El género no puede estar vacío")
            kwargs["genero_libro"] = kwargs["genero_libro"].strip()

        libro.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(libro, key):
                setattr(libro, key, value)

        self.database.commit()
        self.database.refresh(libro)
        return libro

    def cambiar_disponibilidad(
        self, id_libro: UUID, disponible: bool, id_usuario_edita: UUID
    ) -> Optional[Libro]:
        """
        Cambia la disponibilidad de un libro (True = disponible, False = prestado).

        Args:
            id_libro:         UUID del libro.
            disponible:       Nuevo estado de disponibilidad.
            id_usuario_edita: UUID del usuario que realiza el cambio.

        Returns:
            Libro actualizado o None si no existe.
        """
        return self.actualizar_libro(
            id_libro,
            id_usuario_edita,
            disponibilidad_material=disponible,
        )

    def eliminar_libro(self, id_libro: UUID) -> bool:
        """
        Elimina un libro y su registro en materiales_biblioteca.

        Al eliminar, SQLAlchemy borra en cascada ambas tablas
        (libros y materiales_biblioteca) en el orden correcto.

        Args:
            id_libro: UUID del libro a eliminar.

        Returns:
            True si se eliminó correctamente, False si no existe.
        """
        libro = self.obtener_libro(id_libro)
        if libro:
            self.database.delete(libro)
            self.database.commit()
            return True
        return False
