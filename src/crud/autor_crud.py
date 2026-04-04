import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional, Any
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import config
from src.entities.Autor import Autor


class AutorCRUD:
    """
    Clase encargada de gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para la entidad Autor en la base de datos.
    """

    def __init__(self, db_session: Optional[Session] = None):
        """
        Inicializa la clase con una sesión de base de datos.

        Args:
            db_session (Optional[Session]): Sesión de SQLAlchemy. Si no se provee,
                                            se obtiene una por defecto desde la configuración.
        """
        self.db = db_session or config.get_db()

    def crear_autor(
        self,
        nombre_autor: str,
        id_usuario_sesion: str,
        apellido_autor: Optional[str] = None,
        nacionalidad: Optional[str] = None,
    ) -> Optional[Autor]:
        """
        Registra un nuevo autor en el sistema. Por defecto, el autor se crea
        con estado 'activo' en True.

        Args:
            nombre_autor (str): Nombre del autor.
            id_usuario_sesion (str): UUID del usuario que registra al autor (Auditoría).
            apellido_autor (Optional[str], optional): Apellido del autor. Por defecto es None.
            nacionalidad (Optional[str], optional): Nacionalidad del autor. Por defecto es None.

        Returns:
            Optional[Autor]: El objeto Autor creado, o None si ocurre un error.
        """
        print(f"--- Registrando al autor: {nombre_autor} {apellido_autor or ''} ---")

        nuevo_autor = Autor(
            nombre_autor=nombre_autor,
            apellido_autor=apellido_autor,
            nacionalidad=nacionalidad,
            id_usuario_crea=id_usuario_sesion,
            activo=True,
        )

        try:
            self.db.add(nuevo_autor)
            self.db.commit()
            self.db.refresh(nuevo_autor)
            print(f"Autor creado exitosamente. ID: {nuevo_autor.id_autor}")
            return nuevo_autor
        except IntegrityError as e:
            self.db.rollback()
            print(f"Error de integridad al crear autor: {e}")
            return None
        except Exception as e:
            self.db.rollback()
            print(f"Error inesperado: {e}")
            return None

    def obtener_todos_los_autores(self, skip: int = 0, limit: int = 100) -> List[Autor]:
        """
        Recupera todos los autores que están actualmente activos en el sistema.

        Args:
            skip (int): Indica la posición desde donde se muestran los resultados de la base de datos. Por defecto en la posición 0
            limit (int): Indica el máximo de resultados que se van a mostrar. Por defecto 100

        Returns:
            List[Autor]: Lista de objetos Autor con activo == True.
        """
        return (
            self.db.query(Autor)
            .filter(Autor.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def consultar_autor_por_id(self, id_autor_ingresado: str) -> Optional[Autor]:
        """
        Busca un autor específico por su ID, siempre y cuando esté activo.

        Args:
            id_autor_ingresado (str): El ID del autor a buscar.

        Returns:
            Optional[Autor]: El autor encontrado, o None si no existe o está inactivo.
        """
        return (
            self.db.query(Autor)
            .filter(Autor.id_autor == id_autor_ingresado, Autor.activo == True)
            .first()
        )

    def buscar_autor_por_nombre(self, termino_busqueda: str) -> List[Autor]:
        """
        Busca autores activos cuyas coincidencias de nombre o apellido
        contengan el término de búsqueda.

        Args:
            termino_busqueda (str): Fragmento de texto a buscar en nombre o apellido.

        Returns:
            List[Autor]: Lista de autores que coinciden con la búsqueda.
        """
        patron = f"%{termino_busqueda}%"
        return (
            self.db.query(Autor)
            .filter(
                Autor.activo == True,
                or_(
                    Autor.nombre_autor.ilike(patron), Autor.apellido_autor.ilike(patron)
                ),
            )
            .all()
        )

    def actualizar_autor(
        self, id_autor: str, id_usuario_sesion: str, **kwargs: Any
    ) -> Optional[Autor]:
        """
        Actualiza los campos de un autor de forma dinámica. Protege el campo 'id_autor'
        para evitar modificaciones accidentales en la llave primaria.

        Args:
            id_autor (str): ID del autor a modificar.
            id_usuario_sesion (str): UUID del usuario que realiza la edición (Auditoría).
            **kwargs: Pares clave-valor con los campos a actualizar.

        Returns:
            Optional[Autor]: El autor actualizado, o None si no se encontró.
        """
        autor_encontrado = self.consultar_autor_por_id(id_autor)

        if not autor_encontrado:
            print("Error: No se encontró el autor (o fue eliminado previamente) x_x")
            return None

        # Actualización dinámica protegiendo el ID
        for key, value in kwargs.items():
            if hasattr(autor_encontrado, key) and key != "id_autor":
                setattr(autor_encontrado, key, value)

        autor_encontrado.id_usuario_edita = id_usuario_sesion

        try:
            self.db.commit()
            self.db.refresh(autor_encontrado)
            print(f"Autor '{autor_encontrado.nombre_autor}' actualizado con éxito")
            return autor_encontrado
        except Exception as e:
            self.db.rollback()
            print(f"Error al actualizar el autor: {e}")
            return None

    def eliminar_autor(self, id_autor: str, id_usuario_sesion: str) -> bool:
        """
        Realiza una baja lógica (Soft Delete) del autor. No se borra físicamente
        de la base de datos, sino que se marca su campo 'activo' como False.

        Args:
            id_autor (str): ID del autor a dar de baja.
            id_usuario_sesion (str): UUID del usuario que realiza la acción (Auditoría).

        Returns:
            bool: True si la baja lógica fue exitosa, False en caso contrario.
        """
        autor_encontrado = self.consultar_autor_por_id(id_autor)

        if not autor_encontrado:
            print("Error: El autor no existe o ya estaba dado de baja.")
            return False

        autor_encontrado.activo = False
        autor_encontrado.id_usuario_edita = id_usuario_sesion

        try:
            self.db.commit()
            print(
                f"Autor {autor_encontrado.nombre_autor} dado de baja lógicamente (Soft Delete) 👻"
            )
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error al dar de baja al autor: {e}")
            return False
