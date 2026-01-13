from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, auth

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/token")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(database.UsuarioDB).filter(database.UsuarioDB.username == data.username).first()
    if not user or not auth.verificar_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Error de usuario o clave")
    
    token = auth.crear_token_acceso(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}