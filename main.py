from src.database.config import create_tables

from src.entities import (
    Usuario,
    Autor,
    MaterialBiblioteca,
    Libro,
    Revista,
    Periodico,
    Prestamo,
    Reserva,
    Sancion,
)

if __name__ == "__main__":
    create_tables()
    print("Tablas verificadas correctamente en Neon.")
