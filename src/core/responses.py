"""
Esquema de respuesta estándar para la API.

Define el modelo RespuestaAPI, que unifica la estructura de todas las
respuestas exitosas de la aplicación, complementando el manejo de errores
centralizado en error_handlers.py.
"""

from typing import Any, Optional
from pydantic import BaseModel


class RespuestaAPI(BaseModel):
    """
    Modelo de respuesta uniforme para los endpoints de la API.

    Estandariza el formato JSON de salida, facilitando el consumo desde
    clientes y el manejo consistente de respuestas exitosas.

    Attributes:
        mensaje: Descripción breve del resultado de la operación.
        exito: Indica si la operación se completó satisfactoriamente.
        datos: Carga útil opcional de la respuesta. Puede ser cualquier
               tipo serializable (objeto, lista, escalar, etc.).

    Example:
        return RespuestaAPI(
            mensaje="Libro creado exitosamente.",
            exito=True,
            datos=libro,
        )
    """

    mensaje: str
    exito: bool
    datos: Optional[Any] = None
