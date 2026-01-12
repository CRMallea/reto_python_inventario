from fastapi import FastAPI
import database
# Importamos todos nuestros routers
from routers import productos, categorias, admin, usuarios 

app = FastAPI(
    title="Inventario Profesional API",
    version="2.1.0"
)

# Creamos las tablas en SQLite al arrancar
database.Base.metadata.create_all(bind=database.engine)

# Registramos cada módulo de rutas
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(admin.router)
app.include_router(usuarios.router)

@app.get("/")
def home():
    return {"status": "Online", "msg": "API modular funcionando correctamente"}
