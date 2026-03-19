# 📚 Backend-Sistema-De-Biblioteca

Sistema de gestión de biblioteca desarrollado con Python y SQLAlchemy ORM, conectado a una base de datos PostgreSQL en la nube mediante Neon. Permite gestionar materiales bibliográficos (libros, revistas y periódicos), autores y usuarios a través de un menú interactivo en consola.

---

## 🎥 Video demostrativo

[Ver video en Google Drive](https://drive.google.com/file/d/1EC24wAs8_OfUtjiaeUPHPHCkHseHpRR3/view?usp=sharing)

---

## 👥 Equipo

- Cristóbal Mejía Monsalve
- Yulieth Tatiana Muñoz
- Sebastián Torres Cárdenas

---

## 🗂️ Estructura del proyecto

```
Backend-Sistema-De-Biblioteca/
├── alembic/
│   ├── versions/          # Migraciones generadas
│   ├── env.py             # Configuración de Alembic
│   └── script.py.mako     # Plantilla de migraciones
├── src/
│   ├── crud/              # Operaciones CRUD por entidad
│   │   ├── autor_crud.py
│   │   ├── libro_crud.py
│   │   ├── periodico_crud.py
│   │   ├── prestamo_crud.py
│   │   ├── Reserva_crud.py
│   │   ├── Revista_crud.py
│   │   ├── Sancion_crud.py
│   │   └── usuario_crud.py
│   ├── database/
│   │   └── config.py      # Conexión a Neon y configuración de SQLAlchemy
│   ├── entities/          # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py
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
│   └── utils/
│       └── security.py    # Hasheo y verificación de contraseñas
├── .env.example           # Plantilla de variables de entorno
├── .gitignore
├── alembic.ini            # Configuración principal de Alembic
├── main.py                # Punto de entrada y menú interactivo
└── requirements.txt       # Dependencias del proyecto
```

---

## 🧩 Entidades

| Entidad | Descripción |
|---|---|
| `Usuario` | Usuarios del sistema con roles `Admin` y `Usuario` |
| `Autor` | Autores de los materiales bibliográficos |
| `MaterialBiblioteca` | Entidad padre de los materiales (herencia por tabla unida) |
| `Libro` | Subtipo de material con ISBN y género literario |
| `Revista` | Subtipo de material con volumen y número de edición |
| `Periodico` | Subtipo de material con ciudad y sección de publicación |
| `Prestamo` | Registro de préstamos realizados por los usuarios |
| `Reserva` | Reservas de materiales pendientes de disponibilidad |
| `Sancion` | Restricciones temporales aplicadas a usuarios |

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Backend-Sistema-De-Biblioteca.git
cd Backend-Sistema-De-Biblioteca
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` y renómbralo a `.env`, luego completa con tus credenciales de Neon:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg://usuario:contraseña@host/nombre_bd?sslmode=require&channel_binding=require
```

### 5. Ejecutar el proyecto

```bash
python main.py
```

---

## 🗄️ Migraciones con Alembic

Para generar una nueva migración tras modificar un modelo:

```bash
python -m alembic revision --autogenerate -m "descripcion_del_cambio"
python -m alembic upgrade head
```

Para verificar el estado actual:

```bash
python -m alembic current
```

---

## 🛠️ Tecnologías utilizadas

- **Python 3.12+**
- **SQLAlchemy 2.0** — ORM y manejo de sesiones
- **psycopg (psycopg3)** — Driver para PostgreSQL
- **Neon** — Base de datos PostgreSQL en la nube
- **Alembic** — Migraciones de base de datos
- **python-dotenv** — Manejo de variables de entorno