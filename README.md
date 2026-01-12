# 📦 Sistema de Gestión de Inventario API + Streamlit

Este es un sistema full-stack que incluye una **API robusta** con FastAPI y una **interfaz visual** moderna con Streamlit.

## 🚀 Características
- **Autenticación JWT:** Seguridad profesional con tokens.
- **Base de Datos:** SQLite gestionado con SQLAlchemy.
- **Frontend Interactivo:** Visualización de stock y gestión de productos.
- **Seguridad:** Hashing de contraseñas con bcrypt.

## 🛠️ Instalación
1. Clona el repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`.
3. Crea un archivo `.env` con tu `SECRET_KEY`.

## ⚙️ Ejecución
Debes abrir dos terminales:
- **Terminal 1 (Backend):** `uvicorn main:app --reload`
- **Terminal 2 (Frontend):** `streamlit run app_visual.py`
