# 📚 Backend — Sistema de Biblioteca

Backend de una API REST para la gestión de una biblioteca, desarrollado con **FastAPI** y **SQLAlchemy**, con base de datos **PostgreSQL** en Neon y migraciones gestionadas con **Alembic**.

---

## 🎬 Video demostrativo

> **[▶ Ver demostración de la API](https://drive.google.com/file/d/1vk7TvgSvqoMTgWyL_Ylm0YznWRKujL5A/view?usp=sharing)**

---

## 👥 Equipo de desarrollo

| Nombre |
|---|
| Cristóbal Mejía Monsalve |
| Yulieth Tatiana Muñoz |
| Sebastián Torres Cárdenas |

---

## 🛠️ Tecnologías

- **Python 3.11+**
- **FastAPI** — Framework web para la API REST
- **SQLAlchemy** — ORM para el manejo de entidades y relaciones
- **Alembic** — Migraciones de base de datos
- **Pydantic** — Validación de esquemas de entrada y salida
- **PostgreSQL (Neon)** — Base de datos en la nube

---

## 📁 Estructura del proyecto

```
Backend-Sistema-de-Biblioteca/
│
├── migrations/                  # Migraciones de Alembic
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── src/
│   ├── core/                    # Lógica transversal
│   │   ├── error_handlers.py    # Manejadores globales de excepciones
│   │   ├── exceptions.py        # Jerarquía de excepciones de dominio
│   │   └── responses.py         # Esquema de respuesta estándar
│   │
│   ├── crud/                    # Operaciones de base de datos
│   │   ├── autor_crud.py
│   │   ├── libro_crud.py
│   │   ├── periodico_crud.py
│   │   ├── prestamo_crud.py
│   │   ├── Reserva_crud.py
│   │   ├── Revista_crud.py
│   │   ├── Sancion_crud.py
│   │   └── usuario_crud.py
│   │
│   ├── database/                # Configuración de la base de datos
│   │   └── config.py
│   │
│   ├── entities/                # Modelos ORM (SQLAlchemy)
│   │   ├── Auditoria.py
│   │   ├── Autor.py
│   │   ├── Libro.py
│   │   ├── MaterialBiblioteca.py
│   │   ├── Periodico.py
│   │   ├── Prestamo.py
│   │   ├── Reserva.py
│   │   ├── Revista.py
│   │   ├── Sancion.py
│   │   └── Usuario.py
│   │
│   ├── routers/                 # Endpoints de la API
│   │   ├── autor_router.py
│   │   ├── libro_router.py
│   │   ├── periodico_router.py
│   │   ├── prestamo_router.py
│   │   ├── reserva_router.py
│   │   ├── revista_router.py
│   │   ├── sancion_router.py
│   │   └── usuario_router.py
│   │
│   ├── schemas/                 # Esquemas Pydantic (request/response)
│   │   ├── autor_schema.py
│   │   ├── libro_schema.py
│   │   ├── periodico_schema.py
│   │   ├── prestamo_schema.py
│   │   ├── reserva_schema.py
│   │   ├── revista_schema.py
│   │   ├── sancion_schema.py
│   │   └── usuario_schema.py
│   │
│   └── utils/                   # Utilidades
│       └── security.py          # Seguridad y autenticación (JWT)
│
├── app.py                       # Configuración de la aplicación FastAPI
├── main.py                      # Punto de entrada
├── alembic.ini                  # Configuración de Alembic
├── requirements.txt
└── .env.example
```

---

## ⚙️ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/sebastiant01/Backend-Sistema-De-Biblioteca.git
cd Backend-Sistema-De-Biblioteca
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y completa los valores:

```bash
cp .env.example .env
```

Edita `.env` con las credenciales de tu base de datos Neon y demás configuraciones necesarias.
Nota: La URL de la base de datos está estructurada para psycopg3, de tener otra versión, cambiarla.

### 5. Ejecutar las migraciones

```bash
alembic upgrade head
```

### 6. Iniciar el servidor

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`.

La documentación interactiva estará en `http://localhost:8000/docs`.

---

## 📌 Recursos principales de la API

| Recurso | Prefijo |
|---|---|
| Autores | `/autores` |
| Libros | `/libros` |
| Periódicos | `/periodicos` |
| Revistas | `/revistas` |
| Usuarios | `/usuarios` |
| Préstamos | `/prestamos` |
| Reservas | `/reservas` |
| Sanciones | `/sanciones` |