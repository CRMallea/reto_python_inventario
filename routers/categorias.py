from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import database
import schemas
import auth

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

# 1. LISTAR TODAS LAS CATEGORÍAS
@router.get("/", response_model=List[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(database.get_db)):
    return db.query(database.CategoriaDB).all()

# 2. CREAR CATEGORÍA (Protegido)
@router.post("/", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    item: schemas.CategoriaBase, 
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    # Verificamos si el nombre ya existe para evitar duplicados
    nombre_mayus = item.nombre.upper()
    existe = db.query(database.CategoriaDB).filter(database.CategoriaDB.nombre == nombre_mayus).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="Esta categoría ya existe")

    nueva_categoria = database.CategoriaDB(nombre=nombre_mayus)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

# 3. ELIMINAR CATEGORÍA (Borrado Físico con Validación)
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int, 
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    categoria = db.query(database.CategoriaDB).filter(database.CategoriaDB.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # VALIDACIÓN PRO: ¿Tiene productos asociados?
    # Usamos la relación definida en database.py
    if len(categoria.productos) > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"No puedes eliminar esta categoría porque tiene {len(categoria.productos)} productos vinculados. Borra o mueve los productos primero."
        )

    db.delete(categoria)
    db.commit()
    return {"message": "Categoría eliminada con éxito"}