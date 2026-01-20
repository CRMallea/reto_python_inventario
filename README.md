# 📦 Sistema de Gestión de Inventario (FastAPI + Streamlit)

Este proyecto es una solución integral para la gestión de productos y categorías, con un backend robusto en **FastAPI** y una interfaz intuitiva en **Streamlit**.

## 🚀 Características
- **Seguridad**: Autenticación basada en JWT (JSON Web Tokens).
- **Base de Datos**: Persistencia en SQLite mediante SQLAlchemy.
- **Frontend**: Panel de control interactivo con visualización de datos en Pandas.
- **API**: Documentación automática con Swagger UI.
Módulos de Análisis Logístico
El sistema implementa lógica de negocio avanzada para el área de suministros:
1. Control de Reposición (Reorder Point)El sistema audita automáticamente cada producto y asigna un estado:
REPOSICIÓN:(rojo) Productos con stock  menor a 5 unidades. 
OK:(verde) Stock saludable para la operación.
2. Visualización de Inversión: A través de gráficos dinámicos en Plotly, se puede identificar rápidamente qué productos representan la mayor inversión de capital inmovilizado

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


