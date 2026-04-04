"""
Manejadores de excepciones para la aplicación FastAPI.

Centraliza el manejo de errores registrando handlers globales para:
- AppException y sus subclases (errores de dominio de la aplicación).
- ValueError (errores de validación no capturados por Pydantic).
- Exception (cualquier error no previsto, retorna HTTP 500).
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import AppException


def registrar_error_handlers(app: FastAPI) -> None:
    """
    Registra los manejadores de errores globales en la instancia de FastAPI.

    Cada handler captura un tipo de excepción y retorna una respuesta JSON
    uniforme con los campos `mensaje` y `exito`.

    Args:
        app: Instancia de la aplicación FastAPI sobre la que se registran
             los handlers.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """
        Maneja excepciones de dominio derivadas de AppException.

        Retorna el código HTTP y el mensaje definidos en la excepción.
        """
        return JSONResponse(
            status_code=exc.codigo_http,
            content={
                "mensaje": exc.mensaje,
                "exito": False,
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """
        Maneja errores de valor no capturados por Pydantic.

        Retorna siempre HTTP 400 con el mensaje de la excepción.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": str(exc),
                "exito": False,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Maneja cualquier excepción no prevista por los handlers anteriores.

        Retorna HTTP 500 con un mensaje genérico para no exponer detalles internos.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "mensaje": "Error interno del servidor",
                "exito": False,
            },
        )
