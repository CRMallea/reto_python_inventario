from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import database
import schemas
import auth

router = APIRouter(
    prefix="/admin",
    tags=["Administración"]
)

# 1. VER LA PAPELERA (Productos con activo=False)
@router.get("/papelera", response_model=List[schemas.ProductoResponse])
def ver_papelera(
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    productos_borrados = db.query(database.ProductoDB).filter(database.ProductoDB.activo == False).all()
    return productos_borrados

# 2. RESTAURAR PRODUCTO
@router.patch("/restaurar/{producto_id}", response_model=schemas.ProductoResponse)
def restaurar_producto(
    producto_id: int, 
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    producto = db.query(database.ProductoDB).filter(database.ProductoDB.id == producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="El producto no existe")
    
    if producto.activo:
        return producto # Ya está activo, no hacemos nada

    producto.activo = True
    db.commit()
    db.refresh(producto)
    return producto

# 3. VACIAR PAPELERA (Borrado físico permanente)
@router.delete("/papelera/vaciar", status_code=status.HTTP_200_OK)
def vaciar_papelera(
    db: Session = Depends(database.get_db),
    _ = Depends(auth.validar_llave)
):
    # Buscamos todos los inactivos
    consulta = db.query(database.ProductoDB).filter(database.ProductoDB.activo == False)
    conteo = consulta.count()
    
    if conteo == 0:
        return {"message": "La papelera ya está vacía"}
        
    consulta.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"Se han eliminado permanentemente {conteo} productos."}