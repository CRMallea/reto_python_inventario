from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, schemas, auth

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# RUTA 1: REGISTRAR USUARIO
@router.post("/register", response_model=schemas.UsuarioResponse)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Verificar si el usuario ya existe
    existe = db.query(database.UsuarioDB).filter(database.UsuarioDB.username == usuario.username).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    # ENCRIPTAR CONTRASEÑA
    hashed = auth.obtener_password_hash(usuario.password)
    
    nuevo_usuario = database.UsuarioDB(
        username=usuario.username,
        email=usuario.email,
        password_hashed=hashed
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# RUTA 2: LOGIN (Genera el Token JWT)
@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    usuario = db.query(database.UsuarioDB).filter(database.UsuarioDB.username == form_data.username).first()
    
    if not usuario or not auth.verificar_password(form_data.password, usuario.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Crear el Token
    access_token = auth.crear_token_acceso(data={"sub": usuario.username})
    return {"access_token": access_token, "token_type": "bearer"}