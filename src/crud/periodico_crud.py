"""
Operaciones CRUD para Periodico.

Gestiona la creación, lectura, actualización y eliminación de periódicos,
teniendo en cuenta la herencia por tabla unida con MaterialBiblioteca.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy.orm import Session

from src.entities.Periodico import Periodico


class PeriodicoCRUD:
    def __init__(self, database: Session):
        self.database = database

    def crear_periodico(
        self,
        codigo_periodico: str,
        titulo_periodico: str,
        id_autor: UUID,
        ciudad_publicacion: str,
        seccion_periodico: str,
        id_usuario_crea: UUID,
        disponibilidad_periodico: bool = True,
        descripcion_periodico: Optional[str] = None,
        fecha_periodico: Optional[date] = None,
    ) -> Periodico:
        """
        Crea un nuevo periódico en la base de datos.

        Inserta automáticamente en materiales_biblioteca y periodicos
        gracias a la herencia por tabla unida. tipo_material se
        asigna automáticamente como TipoMaterial.periodico.

        Args:
            codigo_periodico:         Código interno único del periódico.
            titulo_periodico:         Nombre del periódico.
            id_autor:                 UUID del autor o entidad responsable.
            ciudad_publicacion:       Ciudad donde se publica el periódico.
            seccion_periodico:        Sección del periódico (deportes, política, etc.).
            id_usuario_crea:          UUID del usuario que registra el periódico.
            disponibilidad_periodico: Disponibilidad inicial (True por defecto).
            descripcion_periodico:    Descripción opcional del periódico.
            fecha_periodico:          Fecha de publicación de la edición.

        Returns:
            Periodico: Instancia del periódico recién creado.

        Raises:
            ValueError: Si algún campo obligatorio es inválido o ya existe.
        """
        if not codigo_periodico or len(codigo_periodico.strip()) == 0:
            raise ValueError("El código del periódico es obligatorio")

        if not titulo_periodico or len(titulo_periodico.strip()) == 0:
            raise ValueError("El título del periódico es obligatorio")

        if not ciudad_publicacion or len(ciudad_publicacion.strip()) == 0:
            raise ValueError("La ciudad de publicación es obligatoria")

        if not seccion_periodico or len(seccion_periodico.strip()) == 0:
            raise ValueError("La sección del periódico es obligatoria")

        if not id_autor:
            raise ValueError("El ID del autor correspondiente es obligatorio")

        if not id_usuario_crea:
            raise ValueError("El ID del usuario que lo creó es obligatorio")

        existente_codigo = (
            self.database.query(Periodico)
            .filter(Periodico.codigo_material == codigo_periodico.strip())
            .first()
        )

        if existente_codigo:
            raise ValueError(
                f"Ya existe un periódico con el código '{codigo_periodico}'"
            )

        nuevo_periodico = Periodico(
            codigo_material=codigo_periodico.strip(),
            titulo_material=titulo_periodico.strip(),
            disponibilidad_material=disponibilidad_periodico,
            descripcion_material=descripcion_periodico,
            fecha_material=fecha_periodico,
            id_autor=id_autor,
            id_usuario_crea=id_usuario_crea,
            ciudad_publicacion=ciudad_publicacion.strip(),
            seccion_periodico=seccion_periodico.strip(),
        )

        self.database.add(nuevo_periodico)
        self.database.commit()
        self.database.refresh(nuevo_periodico)
        return nuevo_periodico

        def obtener_periodico(self, id_periodico: UUID) -> Optional[Periodico]:
            """
            Obtiene un periódico por su UUID.

            Realiza automáticamente el JOIN entre materiales_biblioteca y periodicos.

            Args:
                id_periodico: UUID del periódico a buscar.

            Returns:
                Periodico encontrado o None si no existe.
            """
            return (
                self.database.query(Periodico)
                .filter(Periodico.id_periodico == id_periodico)
                .first()
            )

    def obtener_periodicos(self, skip: int = 0, limit: int = 100) -> List[Periodico]:
        """
        Obtiene una lista paginada de todos los periódicos.

        Args:
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de periódicos.
        """
        return self.database.query(Periodico).offset(skip).limit(limit).all()

    def obtener_periodico_codigo(self, codigo_periodico: str) -> Optional[Periodico]:
        """
        Obtiene un periodico por su código.

        Args:
            codigo_periodico: Código del periódico.

        Returns:
            Periodico encontrado o None si no existe.
        """
        return (
            self.database.query(Periodico)
            .filter(Periodico.codigo_material == codigo_periodico)
            .first
        )

    def obtener_periodicos_por_autor(self, id_autor: UUID) -> List[Periodico]:
        """
        Obtiene todos los periódicos de un autor específico.

        Args:
            id_autor: UUID del autor.

        Returns:
            Lista de periódicos del autor.
        """
        return (
            self.database.query(Periodico).filter(Periodico.id_autor == id_autor).all()
        )

    def obtener_periodicos_por_ciudad(self, ciudad_publicacion: str) -> List[Periodico]:
        """
        Obtiene todos los periódicos de una ciudad de publicación específica.

        Args:
            ciudad_publicacion: Ciudad de publicación a filtrar.

        Returns:
            Lista de periódicos de esa ciudad.
        """
        return (
            self.database.query(Periodico)
            .filter(Periodico.ciudad_publicacion.ilike(f"%{ciudad_publicacion}%"))
            .all()
        )

    def obtener_periodicos_por_seccion(self, seccion_periodico: str) -> List[Periodico]:
        """
        Obtiene todos los periódicos de una sección específica.

        Args:
            seccion_periodico: Sección a filtrar (deportes, política, etc.).

        Returns:
            Lista de periódicos de esa sección.
        """
        return (
            self.database.query(Periodico)
            .filter(Periodico.seccion_periodico.ilike(f"%{seccion_periodico}%"))
            .all()
        )

    def obtener_periodicos_disponibles(self) -> List[Periodico]:
        """
        Obtiene todos los periódicos disponibles para préstamo.

        Returns:
            Lista de periódicos con disponibilidad_material en True.
        """
        return (
            self.database.query(Periodico)
            .filter(Periodico.disponibilidad_material == True)
            .all()
        )

    def buscar_periodicos_por_titulo(self, titulo_periodico: str) -> List[Periodico]:
        """
        Busca periódicos por título (búsqueda parcial, sin distinguir mayúsculas).

        Args:
            titulo_periodico: Texto a buscar en el título.

        Returns:
            Lista de periódicos que coinciden con el título.
        """
        return (
            self.database.query(Periodico)
            .filter(Periodico.titulo_material.ilike(f"%{titulo_periodico}%"))
            .all()
        )

    def actualizar_periodico(
        self,
        id_periodico: UUID,
        id_usuario_edita: UUID,
        **kwargs,
    ) -> Optional[Periodico]:
        """
        Actualiza los campos de un periódico existente.

        Las claves de kwargs deben coincidir con los nombres de atributos
        del ORM (titulo_material, ciudad_publicacion, seccion_periodico, etc.).
        id_usuario_edita es obligatorio para la trazabilidad de auditoría.

        Args:
            id_periodico:     UUID del periódico a actualizar.
            id_usuario_edita: UUID del usuario que realiza la modificación.
            **kwargs:         Campos a actualizar.

        Returns:
            Periodico actualizado o None si no existe.

        Raises:
            ValueError: Si algún campo tiene un valor inválido.
        """
        periodico = self.obtener_periodico(id_periodico)
        if not periodico:
            return None

        if "titulo_material" in kwargs:
            if (
                not kwargs["titulo_material"]
                or len(kwargs["titulo_material"].strip()) == 0
            ):
                raise ValueError("El título no puede estar vacío")
            kwargs["titulo_material"] = kwargs["titulo_material"].strip()

        if "ciudad_publicacion" in kwargs:
            if (
                not kwargs["ciudad_publicacion"]
                or len(kwargs["ciudad_publicacion"].strip()) == 0
            ):
                raise ValueError("La ciudad de publicación no puede estar vacía")
            kwargs["ciudad_publicacion"] = kwargs["ciudad_publicacion"].strip()

        if "seccion_periodico" in kwargs:
            if (
                not kwargs["seccion_periodico"]
                or len(kwargs["seccion_periodico"].strip()) == 0
            ):
                raise ValueError("La sección del periódico no puede estar vacía")
            kwargs["seccion_periodico"] = kwargs["seccion_periodico"].strip()

        periodico.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(periodico, key):
                setattr(periodico, key, value)

        self.database.commit()
        self.database.refresh(periodico)
        return periodico

    def cambiar_disponibilidad(
        self, id_periodico: UUID, disponible: bool, id_usuario_edita: UUID
    ) -> Optional[Periodico]:
        """
        Cambia la disponibilidad de un periódico (True = disponible, False = prestado).

        Args:
            id_periodico:     UUID del periódico.
            disponible:       Nuevo estado de disponibilidad.
            id_usuario_edita: UUID del usuario que realiza el cambio.

        Returns:
            Periodico actualizado o None si no existe.
        """
        return self.actualizar_periodico(
            id_periodico,
            id_usuario_edita,
            disponibilidad_material=disponible,
        )

    def eliminar_periodico(self, id_periodico: UUID) -> bool:
        """
        Elimina un periódico y su registro en materiales_biblioteca.

        Al eliminar, SQLAlchemy borra en cascada ambas tablas
        (periodicos y materiales_biblioteca) en el orden correcto.

        Args:
            id_periodico: UUID del periódico a eliminar.

        Returns:
            True si se eliminó correctamente, False si no existe.
        """
        periodico = self.obtener_periodico(id_periodico)
        if periodico:
            self.database.delete(periodico)
            self.database.commit()
            return True
        return False
