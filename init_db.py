import database
import auth
from sqlalchemy.orm import Session

def inicializar():
    db = database.SessionLocal()
    
    # 1. Crear las tablas
    database.Base.metadata.create_all(bind=database.engine)

    # 2. Crear usuario administrador (si no existe)
    user_exists = db.query(database.UsuarioDB).filter(database.UsuarioDB.username == "admin").first()
    if not user_exists:
        admin_user = database.UsuarioDB(
            username="admin",
            password_hash=auth.obtener_password_hash("admin123") # Cambia la clave aquí
        )
        db.add(admin_user)
        print("✅ Usuario 'admin' creado con éxito.")

    # 3. Crear una categoría inicial
    cat_exists = db.query(database.CategoriaDB).first()
    if not cat_exists:
        default_cat = database.CategoriaDB(nombre="GENERAL")
        db.add(default_cat)
        print("✅ Categoría 'GENERAL' (ID: 1) creada.")

    db.commit()
    db.close()

if __name__ == "__main__":
    inicializar()