"""
Operaciones CRUD para Revista.

Gestiona la creación, lectura, actualización y eliminación de revistas,
teniendo en cuenta la herencia por tabla unida con MaterialBiblioteca.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from src.entities.Revista import Revista
from sqlalchemy.orm import Session


class RevistaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_revista(
        self,
        codigo_material: str,
        titulo_material: str,
        id_autor: UUID,
        volumen: int,
        numero_edicion: int,
        id_usuario_crea: UUID,
        disponibilidad_material: bool = True,
        descripcion_material: Optional[str] = None,
        fecha_material: Optional[date] = None,
    ) -> Revista:
        """
        Crea una nueva revista en la base de datos.

        Inserta automáticamente en materiales_biblioteca y revistas
        gracias a la herencia por tabla unida. tipo_material se
        asigna automáticamente como TipoMaterial.revista.

        Args:
            codigo_material:        Código interno único de la revista (debe empezar con 'R').
            titulo_material:        Título de la revista.
            id_autor:               UUID del autor o entidad responsable.
            volumen:                Número de volumen de la revista (debe ser mayor a 0).
            numero_edicion:         Número de edición de la revista (debe ser mayor a 0).
            id_usuario_crea:        UUID del usuario que registra la revista (auditoría).
            disponibilidad_material: Disponibilidad inicial (True por defecto).
            descripcion_material:   Descripción opcional de la revista.
            fecha_material:         Fecha de publicación de la edición.

        Returns:
            Revista: Instancia de la revista recién creada.

        Raises:
            ValueError: Si algún campo obligatorio es inválido o ya existe.
        """
        if not codigo_material or len(codigo_material.strip()) == 0:
            raise ValueError("El código de la revista es obligatorio")

        if not codigo_material.strip().startswith("R"):
            raise ValueError("El código de la revista debe comenzar con 'R'")

        if not titulo_material or len(titulo_material.strip()) == 0:
            raise ValueError("El título de la revista es obligatorio")

        if volumen <= 0:
            raise ValueError("El volumen debe ser mayor a 0")

        if numero_edicion <= 0:
            raise ValueError("El número de edición debe ser mayor a 0")

        if not id_autor:
            raise ValueError("El ID del autor es obligatorio")

        if not id_usuario_crea:
            raise ValueError("El ID del usuario que lo creó es obligatorio")

        existente = (
            self.db.query(Revista)
            .filter(Revista.codigo_material == codigo_material.strip())
            .first()
        )
        if existente:
            raise ValueError(f"Ya existe una revista con el código '{codigo_material}'")

        revista = Revista(
            codigo_material=codigo_material.strip(),
            titulo_material=titulo_material.strip(),
            disponibilidad_material=disponibilidad_material,
            descripcion_material=descripcion_material,
            fecha_material=fecha_material,
            id_autor=id_autor,
            id_usuario_crea=id_usuario_crea,
            volumen=volumen,
            numero_edicion=numero_edicion,
        )
        self.db.add(revista)
        self.db.commit()
        self.db.refresh(revista)
        return revista

    def obtener_revista(self, revista_id: UUID) -> Optional[Revista]:
        """
        Obtener una revista por ID.

        Realiza automáticamente el JOIN entre materiales_biblioteca y revistas.

        Args:
            revista_id: UUID de la revista a buscar.

        Returns:
            Revista encontrada o None si no existe.
        """
        return self.db.query(Revista).filter(Revista.id_revista == revista_id).first()

    def obtener_revista_por_codigo(self, codigo_material: str) -> Optional[Revista]:
        """
        Obtener una revista por su código.

        Args:
            codigo_material: Código de la revista.

        Returns:
            Revista encontrada o None si no existe.
        """
        return (
            self.db.query(Revista)
            .filter(Revista.codigo_material == codigo_material)
            .first()
        )

    def obtener_revistas(self, skip: int = 0, limit: int = 100) -> List[Revista]:
        """
        Obtener lista de revistas con paginación.

        Args:
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de revistas.
        """
        return self.db.query(Revista).offset(skip).limit(limit).all()

    def obtener_revistas_por_volumen(
        self, volumen: int, skip: int = 0, limit: int = 100
    ) -> List[Revista]:
        """
        Obtener todas las revistas de un volumen específico.

        Args:
            volumen: Número de volumen a buscar.
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de revistas del volumen indicado.
        """
        return (
            self.db.query(Revista)
            .filter(Revista.volumen == volumen)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_revistas_por_autor(
        self, id_autor: UUID, skip: int = 0, limit: int = 100
    ) -> List[Revista]:
        """
        Obtener todas las revistas de un autor específico.

        Args:
            id_autor: UUID del autor.
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de revistas del autor.
        """
        return (
            self.db.query(Revista)
            .filter(Revista.id_autor == id_autor)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_revistas_por_titulo(
        self, titulo: str, skip: int = 0, limit: int = 100
    ) -> List[Revista]:
        """
        Buscar revistas por título (búsqueda parcial, sin distinguir mayúsculas).

        Args:
            titulo: Texto a buscar en el título.
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de revistas que coinciden con el título.
        """
        return (
            self.db.query(Revista)
            .filter(Revista.titulo_material.ilike(f"%{titulo}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_revistas_disponibles(
        self, skip: int = 0, limit: int = 100
    ) -> List[Revista]:
        """
        Obtener todas las revistas disponibles para préstamo.

        Args:
            skip:  Número de registros a omitir.
            limit: Límite de registros a retornar.

        Returns:
            Lista de revistas con disponibilidad_material en True.
        """
        return (
            self.db.query(Revista)
            .filter(Revista.disponibilidad_material == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def actualizar_revista(
        self, revista_id: UUID, id_usuario_edita: UUID, **kwargs
    ) -> Optional[Revista]:
        """
        Actualizar los campos de una revista existente.

        Args:
            revista_id:       UUID de la revista a actualizar.
            id_usuario_edita: UUID del usuario que realiza la modificación.
            **kwargs:         Campos a actualizar.

        Returns:
            Revista actualizada o None si no existe.

        Raises:
            ValueError: Si algún campo tiene un valor inválido.
        """
        revista = self.obtener_revista(revista_id)
        if not revista:
            return None

        if "titulo_material" in kwargs:
            if (
                not kwargs["titulo_material"]
                or len(kwargs["titulo_material"].strip()) == 0
            ):
                raise ValueError("El título no puede estar vacío")
            kwargs["titulo_material"] = kwargs["titulo_material"].strip()

        if "volumen" in kwargs:
            if kwargs["volumen"] <= 0:
                raise ValueError("El volumen debe ser mayor a 0")

        if "numero_edicion" in kwargs:
            if kwargs["numero_edicion"] <= 0:
                raise ValueError("El número de edición debe ser mayor a 0")

        revista.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(revista, key):
                setattr(revista, key, value)

        self.db.commit()
        self.db.refresh(revista)
        return revista

    def cambiar_disponibilidad(
        self, revista_id: UUID, disponible: bool, id_usuario_edita: UUID
    ) -> Optional[Revista]:
        """
        Cambia la disponibilidad de una revista (True = disponible, False = prestada).

        Args:
            revista_id:       UUID de la revista.
            disponible:       Nuevo estado de disponibilidad.
            id_usuario_edita: UUID del usuario que realiza el cambio.

        Returns:
            Revista actualizada o None si no existe.
        """
        return self.actualizar_revista(
            revista_id,
            id_usuario_edita,
            disponibilidad_material=disponible,
        )

    def eliminar_revista(self, revista_id: UUID) -> bool:
        """
        Elimina una revista y su registro en materiales_biblioteca.

        Al eliminar, SQLAlchemy borra en cascada ambas tablas
        (revistas y materiales_biblioteca) en el orden correcto.

        Args:
            revista_id: UUID de la revista a eliminar.

        Returns:
            True si se eliminó correctamente, False si no existe.
        """
        revista = self.obtener_revista(revista_id)
        if revista:
            self.db.delete(revista)
            self.db.commit()
            return True
        return False
