from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database, auth, schemas

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/")
def listar(db: Session = Depends(database.get_db), user=Depends(auth.obtener_usuario_actual)):
    return db.query(database.ProductoDB).all()

@router.post("/")
def crear(item: schemas.ProductoCreate, db: Session = Depends(database.get_db), user=Depends(auth.obtener_usuario_actual)):
    nuevo = database.ProductoDB(**item.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo