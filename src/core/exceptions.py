"""
Excepciones personalizadas de la aplicación.

Define una jerarquía de excepciones basada en AppException que permite
asociar cada tipo de error de dominio con un código HTTP específico,
simplificando el manejo centralizado en error_handlers.py.
"""

from fastapi import status


class AppException(Exception):
    """
    Excepción base de la aplicación.

    Todas las excepciones de dominio deben heredar de esta clase para ser
    capturadas por el handler global registrado en error_handlers.py.

    Args:
        mensaje: Descripción del error que se retornará al cliente.
        codigo_http: Código de estado HTTP asociado. Por defecto, 400.

    Attributes:
        mensaje (str): Mensaje descriptivo del error.
        codigo_http (int): Código HTTP que se usará en la respuesta.
    """

    def __init__(self, mensaje: str, codigo_http: int = status.HTTP_400_BAD_REQUEST):
        self.mensaje = mensaje
        self.codigo_http = codigo_http
        super().__init__(self.mensaje)


class NoEncontradoError(AppException):
    """
    Se lanza cuando un recurso solicitado no existe en la base de datos.

    Retorna HTTP 404. El mensaje se construye automáticamente a partir
    del nombre de la clase del recurso.

    Args:
        clase: Nombre del recurso no encontrado (ej. "Libro", "Usuario").

    Example:
        raise NoEncontradoError("Libro")
        # → mensaje: "Libro no encontrado/a."  |  HTTP 404
    """

    def __init__(self, clase: str):
        super().__init__(
            mensaje=f"{clase} no encontrado/a.", codigo_http=status.HTTP_404_NOT_FOUND
        )


class DatosInvalidosError(AppException):
    """
    Se lanza ante errores de validación o violaciones de lógica de negocio.

    Retorna HTTP 400 con el detalle del error proporcionado.

    Args:
        mensaje_detalle: Descripción específica del dato inválido o la
                         regla de negocio incumplida.

    Example:
        raise DatosInvalidosError("Campo 'disponibilidad_material' no válido.")
    """

    def __init__(self, mensaje_detalle: str):
        super().__init__(
            mensaje=mensaje_detalle, codigo_http=status.HTTP_400_BAD_REQUEST
        )
