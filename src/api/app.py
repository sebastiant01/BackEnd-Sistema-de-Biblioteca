from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.config import create_tables

from src.routers import (
    reserva_router,
    revista_router,
    autor_router,
    libro_router,
    sancion_router,
    usuario_router,
    prestamo_router,
    periodico_router,
)
from src.core.error_handlers import registrar_error_handlers


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from src.entities import (
        Autor,
        MaterialBiblioteca,
        Libro,
        Periodico,
        Revista,
        Prestamo,
        Reserva,
        Sancion,
        Usuario,
    )

    create_tables()
    yield


app = FastAPI(title="Sistema-De-Biblioteca", version="1.0.0", lifespan=lifespan)

registrar_error_handlers(app=app)

app.include_router(usuario_router.router)
app.include_router(autor_router.router)
app.include_router(libro_router.router)
app.include_router(periodico_router.router)
app.include_router(revista_router.router)
app.include_router(prestamo_router.router)
app.include_router(reserva_router.router)
app.include_router(sancion_router.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
