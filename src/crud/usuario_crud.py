import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from random import randint
from typing import List, Optional, Any
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.utils.security import security
from src.database import config
from src.entities.Usuario import Usuario


class UsuarioCRUD:
    """
    Clase encargada de gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para la entidad Usuario en la base de datos.
    """

    def __init__(self, db_session: Optional[Session] = None):
        """
        Inicializa la clase con una sesión de base de datos.

        Args:
            db_session (Optional[Session]): Sesión de SQLAlchemy. Si no se provee,
                                            se obtiene una por defecto desde la configuración.
        """
        self.db = db_session or config.get_db()

    @staticmethod
    def _crear_username(nombre: str, apellido: str) -> str:
        """
        Genera un username único combinando la primera palabra del nombre,
        la primera palabra del apellido y un número aleatorio de 6 dígitos.

        Args:
            nombre (str): Nombre(s) del usuario.
            apellido (str): Apellido(s) del usuario.

        Returns:
            str: Username generado (ej. 'juanperez123456').
        """
        num = randint(100000, 999999)
        nom = nombre.split()[0].lower()
        ape = apellido.split()[0].lower()
        return f"{nom}{ape}{num}"

    def crear_usuario(
        self,
        nombre_nuevo: str,
        apellido_nuevo: str,
        documento_nuevo: str,
        email_nuevo: str,
        telefono_nuevo: str,
        contrasena_nueva: str,
        rol_nuevo: str = "Usuario",
    ) -> Optional[Usuario]:
        """
        Crea un nuevo usuario en la base de datos hasheando su contraseña y
        asignándole un username automático.

        Args:
            nombre_nuevo (str): Nombre del usuario.
            apellido_nuevo (str): Apellido del usuario.
            documento_nuevo (str): Documento de identidad (debe ser único).
            email_nuevo (str): Correo electrónico (debe ser único).
            telefono_nuevo (str): Número de contacto.
            contrasena_nueva (str): Contraseña en texto plano (será hasheada).
            rol_nuevo (str, optional): Rol del usuario en el sistema. Por defecto es "Usuario".

        Returns:
            Optional[Usuario]: El objeto Usuario creado si es exitoso, o None si hay
                               un error de integridad (ej. documento o email duplicado).
        """
        print("--- Creando usuario ---")

        nuevo_username = self._crear_username(nombre_nuevo, apellido_nuevo)
        contrasena_hasheada = security.hashear_contrasena(contrasena_nueva)

        nuevo_usuario = Usuario(
            nombre=nombre_nuevo,
            apellido=apellido_nuevo,
            documento=documento_nuevo,
            email=email_nuevo,
            telefono=telefono_nuevo,
            username=nuevo_username,
            contrasena=contrasena_hasheada,
            rol=rol_nuevo,
        )

        try:
            self.db.add(nuevo_usuario)
            self.db.commit()
            self.db.refresh(nuevo_usuario)
            print(f"Usuario creado exitosamente: {nuevo_usuario.username}")
            return nuevo_usuario
        except IntegrityError as e:
            self.db.rollback()
            print(f"Error de integridad (¿Documento o email repetido?): {e}")
            return None

    def obtener_todos_los_usuarios(self) -> List[Usuario]:
        """
        Recupera todos los usuarios registrados en la base de datos.

        Returns:
            List[Usuario]: Lista de objetos Usuario.
        """
        return self.db.query(Usuario).all()

    def consultar_usuario_por_id(self, id_ingresado: str) -> Optional[Usuario]:
        """
        Busca un usuario específico mediante su ID único.

        Args:
            id_ingresado (str): El ID del usuario a buscar.

        Returns:
            Optional[Usuario]: El usuario encontrado, o None si no existe.
        """
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_ingresado).first()

    def consultar_usuario_por_username(
        self, username_ingresado: str
    ) -> Optional[Usuario]:
        """
        Busca un usuario específico mediante su username.

        Args:
            username_ingresado (str): El username a buscar.

        Returns:
            Optional[Usuario]: El usuario encontrado, o None si no existe.
        """
        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.username == username_ingresado)
            .first()
        )
        if usuario:
            print(f"Usuario encontrado: {usuario.nombre} {usuario.apellido}")
        return usuario

    def consultar_usuario_por_email(self, email_ingresado: str) -> Optional[Usuario]:
        """
        Busca un usuario específico mediante su correo electrónico.

        Args:
            email_ingresado (str): El email a buscar.

        Returns:
            Optional[Usuario]: El usuario encontrado, o None si no existe.
        """
        return self.db.query(Usuario).filter(Usuario.email == email_ingresado).first()

    def consultar_usuario_por_documento(
        self, documento_ingresado: str
    ) -> Optional[Usuario]:
        """
        Busca un usuario específico mediante su número de documento.

        Args:
            documento_ingresado (str): El documento a buscar.

        Returns:
            Optional[Usuario]: El usuario encontrado, o None si no existe.
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.documento == documento_ingresado)
            .first()
        )

    def consultar_usuario_por_telefono(
        self, telefono_ingresado: str
    ) -> Optional[Usuario]:
        """
        Busca un usuario específico mediante su número de teléfono.

        Args:
            telefono_ingresado (str): El teléfono a buscar.

        Returns:
            Optional[Usuario]: El usuario encontrado, o None si no existe.
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.telefono == telefono_ingresado)
            .first()
        )

    def buscar_usuario_universal(self, termino_busqueda: str) -> List[Usuario]:
        """
        Realiza una búsqueda flexible de usuarios intentando coincidir el término
        ingresado con el nombre, apellido, username, email o documento.

        Args:
            termino_busqueda (str): El texto o fragmento a buscar.

        Returns:
            List[Usuario]: Lista de usuarios que coinciden con el criterio de búsqueda.
        """
        patron = f"%{termino_busqueda}%"
        lista_de_coincidencias = (
            self.db.query(Usuario)
            .filter(
                or_(
                    Usuario.nombre.ilike(patron),
                    Usuario.apellido.ilike(patron),
                    Usuario.username.ilike(patron),
                    Usuario.email.ilike(patron),
                    Usuario.documento.ilike(patron),
                )
            )
            .all()
        )
        return lista_de_coincidencias

    def actualizar_usuario(self, id_usuario: str, **kwargs: Any) -> Optional[Usuario]:
        """
        Actualiza dinámicamente uno o más campos de un usuario existente.
        Si se actualiza la contraseña, esta se hashea automáticamente antes de guardarse.

        Ejemplo de uso:
            crud.actualizar_usuario(id, telefono="300123", rol="Admin")

        Args:
            id_usuario (str): ID del usuario a modificar.
            **kwargs: Pares clave-valor con los campos a actualizar.

        Returns:
            Optional[Usuario]: El usuario actualizado, o None si hubo un error o no se encontró.
        """
        usuario_encontrado = self.consultar_usuario_por_id(id_usuario)

        if not usuario_encontrado:
            print("Error: No se encontró el usuario para actualizar x_x")
            return None

        for key, value in kwargs.items():
            if hasattr(usuario_encontrado, key):
                if key == "contrasena":
                    value = security.hashear_contrasena(value)
                setattr(usuario_encontrado, key, value)

        try:
            self.db.commit()
            self.db.refresh(usuario_encontrado)
            print(f"Usuario {usuario_encontrado.username} actualizado con éxito")
            return usuario_encontrado
        except Exception as e:
            self.db.rollback()
            print(f"Error al actualizar: {e}")
            return None

    def eliminar_usuario(self, id_usuario: str) -> bool:
        """
        Realiza una eliminación física del usuario en la base de datos.
        Nota: Ya que la auditoría usa Soft References, la base de datos no fallará
        por llaves foráneas.

        Args:
            id_usuario (str): ID del usuario a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        usuario_encontrado = self.consultar_usuario_por_id(id_usuario)

        if not usuario_encontrado:
            print("Error: El usuario no existe o ya fue eliminado.")
            return False

        try:
            self.db.delete(usuario_encontrado)
            self.db.commit()
            print("Usuario eliminado del sistema")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error al eliminar usuario: {e}")
            return False
