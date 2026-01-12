from pydantic import BaseModel, Field
from typing import Optional

# --- ESQUEMAS PARA PRODUCTOS ---

class ProductoBase(BaseModel):
    """Campos comunes para crear y leer productos"""
    nombre: str = Field(..., min_length=3, max_length=50, example="Monitor Gamer")
    precio: float = Field(..., gt=0, example=299.99)
    stock: int = Field(..., ge=0, example=10)
    categoria_id: int = Field(..., example=1)

class ProductoCreate(ProductoBase):
    """Se usa cuando recibimos datos del usuario para crear"""
    pass

class ProductoResponse(ProductoBase):
    """Se usa para enviar datos al usuario (incluye el ID y el estado)"""
    id: int
    activo: bool

    class Config:
        from_attributes = True # Permite que Pydantic lea modelos de SQLAlchemy


# --- ESQUEMAS PARA CATEGORÍAS ---

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=30, example="Electrónica")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA USUARIOS ---

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str # El usuario envía la clave normal

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    esta_activo: bool

    class Config:
        from_attributes = True

# Esquema especial para el Token de Login
class Token(BaseModel):
    access_token: str
    token_type: str