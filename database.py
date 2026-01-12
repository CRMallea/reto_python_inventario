from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///./inventario.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para que los routers obtengan la conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MODELOS DE TABLAS
class CategoriaDB(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    productos = relationship("ProductoDB", back_populates="categoria")

class ProductoDB(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("CategoriaDB", back_populates="productos")

# ... (Tus otros modelos CategoriaDB y ProductoDB se quedan igual)

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password_hashed = Column(String) # Aquí va la clave encriptada
    esta_activo = Column(Boolean, default=True)