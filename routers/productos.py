from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importamos nuestros archivos locales
import database
import schemas
import auth

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# 1. LISTAR PRODUCTOS (Solo los activos)
@router.get("/", response_model=List[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(database.get_db)):
    # Traemos de la DB solo los que tienen activo=True
    productos = db.query(database.ProductoDB).filter(database.ProductoDB.activo == True).all()
    return productos

# 2. CREAR UN PRODUCTO (Protegido con API Key)
@router.post("/", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    item: schemas.ProductoCreate, 
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave) # Verificamos la llave antes de entrar
):
    # Validamos si la categoría existe
    categoria = db.query(database.CategoriaDB).filter(database.CategoriaDB.id == item.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="La categoría especificada no existe")

    # Creamos el objeto de base de datos transformando el esquema Pydantic a diccionario
    nuevo_producto = database.ProductoDB(**item.model_dump())
    
    # Forzamos el nombre a mayúsculas como buena práctica de orden
    nuevo_producto.nombre = nuevo_producto.nombre.upper()
    
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

# 3. ELIMINAR UN PRODUCTO (Soft Delete)
@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(
    producto_id: int, 
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    producto = db.query(database.ProductoDB).filter(database.ProductoDB.id == producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # En lugar de borrar de la DB, desactivamos
    producto.activo = False
    db.commit()
    
    return {"message": f"Producto '{producto.nombre}' movido a la papelera"}
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import database  # Importamos el archivo donde está la DB y los modelos
from auth import validar_llave  # <-- CAMBIO AQUÍ
from schemas import Producto   # <-- CAMBIO AQUÍ

# Configuramos el Router
router = APIRouter(
    prefix="/productos",
    tags=["Gestión de Productos"] # Esto agrupa las rutas en Swagger
)

# 1. OBTENER PRODUCTOS ACTIVOS
@router.get("/", response_model=List[dict])
async def listar_productos(db: Session = Depends(database.get_db)):
    productos = db.query(database.ProductoDB).filter(database.ProductoDB.activo == True).all()
    
    # Formateamos la respuesta para incluir el nombre de la categoría
    return [{
        "id": p.id,
        "nombre": p.nombre,
        "precio": p.precio,
        "stock": p.stock,
        "categoria": p.categoria.nombre if p.categoria else "Sin Categoría"
    } for p in productos]

# 2. CREAR PRODUCTO (Protegido)
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(validar_llave)])
async def crear_producto(item: Producto, db: Session = Depends(database.get_db)):
    # Verificar categoría
    cat = db.query(database.CategoriaDB).filter(database.CategoriaDB.id == item.categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    nuevo_p = database.ProductoDB(
        nombre=item.nombre.upper(),
        precio=item.precio,
        stock=item.stock,
        categoria_id=item.categoria_id,
        activo=True
    )
    db.add(nuevo_p)
    db.commit()
    db.refresh(nuevo_p)
    return nuevo_p

# 3. ELIMINAR (SOFT DELETE - Protegido)
@router.delete("/{producto_id}", dependencies=[Depends(validar_llave)])
async def eliminar_producto(producto_id: int, db: Session = Depends(database.get_db)):
    producto = db.query(database.ProductoDB).filter(database.ProductoDB.id == producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.activo = False
    db.commit()
    return {"message": f"Producto '{producto.nombre}' movido a la papelera"}
    """