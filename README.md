# 📦 Sistema de Gestión de Inventario (FastAPI + Streamlit)

Este proyecto es una solución integral para la gestión de productos y categorías, con un backend robusto en **FastAPI** y una interfaz intuitiva en **Streamlit**.

## 🚀 Características
- **Seguridad**: Autenticación basada en JWT (JSON Web Tokens).
- **Base de Datos**: Persistencia en SQLite mediante SQLAlchemy.
- **Frontend**: Panel de control interactivo con visualización de datos en Pandas.
- **API**: Documentación automática con Swagger UI.

## 🛠️ Instalación y Configuración

1. **Clonar o descargar el proyecto** en una carpeta.
2. **Instalar dependencias**:

pip install -r requirements.txt

Inicializar la Base de Datos (Crea el usuario admin y categorías iniciales):

Bash

python init_db.py
🏃 Ejecución
Debes abrir dos terminales diferentes:

Terminal 1: Backend (API)


uvicorn main:app --reload


La API estará disponible en: https://www.google.com/search?q=http://127.0.0.1:8000 Documentación interactiva: https://www.google.com/search?q=http://127.0.0.1:8000/docs

Terminal 2: Frontend (Streamlit)


streamlit run app_visual.py


🔐 Credenciales por defecto

Usuario: admin
Contraseña: admin123


