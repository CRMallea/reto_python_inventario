from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from routers import productos, categorias, usuarios

# Crear tablas
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Inventario Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(categorias.router)

@app.get("/")
def root():
    return {"status": "Online"}
