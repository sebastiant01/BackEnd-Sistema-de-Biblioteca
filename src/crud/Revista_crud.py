"""
Operaciones CRUD para Revista
"""

from typing import List, Optional
from uuid import UUID

from src.entities.Revista import Revista
from sqlalchemy.orm import Session


class RevistaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_revista(
        self,
        id_material: UUID,
        volumen: int,
        numero_edicion: int,
        id_usuario_crea: UUID,
    ) -> Revista:
        """
        Crear una nueva revista con validaciones

        Args:
            id_material: UUID del material padre en MaterialBiblioteca
            volumen: Número de volumen de la revista (debe ser mayor a 0)
            numero_edicion: Número de edición de la revista (debe ser mayor a 0)
            id_usuario_crea: UUID del usuario que registra la operación (auditoría)

        Returns:
            Revista creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if volumen <= 0:
            raise ValueError("El volumen debe ser mayor a 0")

        if numero_edicion <= 0:
            raise ValueError("El número de edición debe ser mayor a 0")

        from src.entities.MaterialBiblioteca import MaterialBiblioteca, TipoMaterial

        material = (
            self.db.query(MaterialBiblioteca)
            .filter(MaterialBiblioteca.id_material == id_material)
            .first()
        )
        if not material:
            raise ValueError("El material especificado no existe")

        if material.tipo_material != TipoMaterial.revista:
            raise ValueError("El material especificado no es de tipo revista")

        if not material.codigo_material.startswith("R"):
            raise ValueError(
                "El código del material debe comenzar con 'R' para revistas"
            )

        revista_existente = (
            self.db.query(Revista).filter(Revista.id_revista == id_material).first()
        )
        if revista_existente:
            raise ValueError("Ya existe una revista asociada a ese material")

        revista = Revista(
            id_revista=id_material,
            volumen=volumen,
            numero_edicion=numero_edicion,
            id_usuario_crea=id_usuario_crea,
            id_usuario_edita=None,
        )
        self.db.add(revista)
        self.db.commit()
        self.db.refresh(revista)
        return revista

    def obtener_revista(self, revista_id: UUID) -> Optional[Revista]:
        """
        Obtener una revista por ID

        Args:
            revista_id: UUID de la revista

        Returns:
            Revista encontrada o None
        """
        return self.db.query(Revista).filter(Revista.id_revista == revista_id).first()

    def obtener_revistas(self, skip: int = 0, limit: int = 100) -> List[Revista]:
        """
        Obtener lista de revistas con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de revistas
        """
        return self.db.query(Revista).offset(skip).limit(limit).all()

    def obtener_revistas_por_volumen(self, volumen: int) -> List[Revista]:
        """
        Obtener todas las revistas de un volumen específico

        Args:
            volumen: Número de volumen a buscar

        Returns:
            Lista de revistas del volumen indicado
        """
        return self.db.query(Revista).filter(Revista.volumen == volumen).all()

    def actualizar_revista(
        self, revista_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Revista]:
        """
        Actualizar una revista con validaciones

        Args:
            revista_id: UUID de la revista
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar (volumen, numero_edicion)

        Returns:
            Revista actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        revista = self.obtener_revista(revista_id)
        if not revista:
            return None

        if "volumen" in kwargs:
            if kwargs["volumen"] <= 0:
                raise ValueError("El volumen debe ser mayor a 0")

        if "numero_edicion" in kwargs:
            if kwargs["numero_edicion"] <= 0:
                raise ValueError("El número de edición debe ser mayor a 0")

        if id_usuario_edita is None:
            from src.entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.rol == "Admin").first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la revista"
                )
            id_usuario_edita = admin.id_usuario

        revista.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(revista, key):
                setattr(revista, key, value)

        self.db.commit()
        self.db.refresh(revista)
        return revista

    def eliminar_revista(self, revista_id: UUID) -> bool:
        """
        Eliminar una revista

        Args:
            revista_id: UUID de la revista

        Returns:
            True si se eliminó, False si no existe
        """
        revista = self.obtener_revista(revista_id)
        if revista:
            self.db.delete(revista)
            self.db.commit()
            return True
        return False
