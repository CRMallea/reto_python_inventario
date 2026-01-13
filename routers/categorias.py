from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database, auth, schemas

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=list[schemas.CategoriaResponse])
def listar(db: Session = Depends(database.get_db), user=Depends(auth.obtener_usuario_actual)):
    return db.query(database.CategoriaDB).all()

@router.post("/", response_model=schemas.CategoriaResponse)
def crear(item: schemas.CategoriaCreate, db: Session = Depends(database.get_db), user=Depends(auth.obtener_usuario_actual)):
    nueva = database.CategoriaDB(nombre=item.nombre.upper())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
