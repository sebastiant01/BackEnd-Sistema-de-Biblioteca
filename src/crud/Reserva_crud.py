"""
Operaciones CRUD para Reserva
"""
 
from typing import List, Optional
from uuid import UUID
 
from src.entities.Reserva import EstadoReserva, Reserva
from sqlalchemy.orm import Session
 
 
class ReservaCRUD:
    def __init__(self, db: Session):
        self.db = db
 
    def crear_reserva(
        self,
        id_usuario: UUID,
        id_material: UUID,
        fecha_reserva: str,
        id_usuario_crea: UUID,
    ) -> Reserva:
        """
        Crear una nueva reserva con validaciones
 
        Args:
            id_usuario: UUID del usuario que realiza la reserva
            id_material: UUID del material que se desea reservar
            fecha_reserva: Fecha en que se entregará el material al usuario
            id_usuario_crea: UUID del usuario que registra la operación (auditoría)
 
        Returns:
            Reserva creada
 
        Raises:
            ValueError: Si los datos no son válidos
        """
        from src.entities.Usuario import Usuario
 
        usuario = (
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if not usuario:
            raise ValueError("El usuario especificado no existe")
 
        from src.entities.MaterialBiblioteca import MaterialBiblioteca
 
        material = (
            self.db.query(MaterialBiblioteca)
            .filter(MaterialBiblioteca.id_material == id_material)
            .first()
        )
        if not material:
            raise ValueError("El material especificado no existe")
 
        if not material.disponibilidad_material:
            raise ValueError("El material no está disponible para reserva")
 
        reserva_existente = (
            self.db.query(Reserva)
            .filter(
                Reserva.id_usuario == id_usuario,
                Reserva.id_material == id_material,
                Reserva.estado_reserva == EstadoReserva.pendiente,
            )
            .first()
        )
        if reserva_existente:
            raise ValueError(
                "El usuario ya tiene una reserva pendiente para este material"
            )
 
        reserva = Reserva(
            id_usuario=id_usuario,
            id_material=id_material,
            fecha_reserva=fecha_reserva,
            id_usuario_crea=id_usuario_crea,
            id_usuario_edita=None,
        )
        material.disponibilidad_material = False
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
 
    def obtener_reserva(self, reserva_id: UUID) -> Optional[Reserva]:
        """
        Obtener una reserva por ID
 
        Args:
            reserva_id: UUID de la reserva
 
        Returns:
            Reserva encontrada o None
        """
        return self.db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
 
    def obtener_reservas(self, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """
        Obtener lista de reservas con paginación
 
        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
 
        Returns:
            Lista de reservas
        """
        return self.db.query(Reserva).offset(skip).limit(limit).all()
 
    def obtener_reservas_por_usuario(
        self, id_usuario: UUID, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener todas las reservas de un usuario específico
 
        Args:
            id_usuario: UUID del usuario
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
 
        Returns:
            Lista de reservas del usuario
        """
        return (
            self.db.query(Reserva)
            .filter(Reserva.id_usuario == id_usuario)
            .offset(skip)
            .limit(limit)
            .all()
        )
 
    def obtener_reservas_por_material(
        self, id_material: UUID, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener todas las reservas de un material específico
 
        Args:
            id_material: UUID del material
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
 
        Returns:
            Lista de reservas del material
        """
        return (
            self.db.query(Reserva)
            .filter(Reserva.id_material == id_material)
            .offset(skip)
            .limit(limit)
            .all()
        )
 
    def obtener_reservas_por_estado(
        self, estado: EstadoReserva, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener todas las reservas filtradas por estado
 
        Args:
            estado: Estado de la reserva (EstadoReserva.pendiente, etc.)
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
 
        Returns:
            Lista de reservas con el estado indicado
        """
        return (
            self.db.query(Reserva)
            .filter(Reserva.estado_reserva == estado)
            .offset(skip)
            .limit(limit)
            .all()
        )
 
    def actualizar_reserva(
        self, reserva_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Reserva]:
        """
        Actualizar una reserva con validaciones
 
        Args:
            reserva_id: UUID de la reserva
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar
 
        Returns:
            Reserva actualizada o None
 
        Raises:
            ValueError: Si los datos no son válidos
        """
        reserva = self.obtener_reserva(reserva_id)
        if not reserva:
            return None
 
        if "estado_reserva" in kwargs:
            try:
                kwargs["estado_reserva"] = EstadoReserva(kwargs["estado_reserva"])
            except ValueError:
                raise ValueError("El estado debe ser un valor válido de EstadoReserva")
 
        if id_usuario_edita is None:
            from src.entities.Usuario import Usuario
 
            admin = self.db.query(Usuario).filter(Usuario.rol == "Admin").first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la reserva"
                )
            id_usuario_edita = admin.id_usuario
 
        reserva.id_usuario_edita = id_usuario_edita
 
        for key, value in kwargs.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)
 
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
 
    def eliminar_reserva(self, reserva_id: UUID) -> bool:
        """
        Eliminar una reserva
 
        Args:
            reserva_id: UUID de la reserva
 
        Returns:
            True si se eliminó, False si no existe
        """
        reserva = self.obtener_reserva(reserva_id)
        if reserva:
            self.db.delete(reserva)
            self.db.commit()
            return True
        return False