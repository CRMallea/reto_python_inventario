import database
from sqlalchemy.orm import Session

def cargar_datos_prueba():
    # Creamos la sesión manualmente desde la fábrica SessionLocal
    db = database.SessionLocal()
    
    try:
        print("--- Iniciando siembra de datos ---")

        # 1. Limpieza segura: Borrar productos y luego categorías
        # (Se hace en ese orden por la llave foránea)
        db.query(database.ProductoDB).delete()
        db.query(database.CategoriaDB).delete()
        db.commit()
        print("✅ Base de datos limpia.")

        # 2. Crear instancias de Categorías
        cat1 = database.CategoriaDB(nombre="ELECTRÓNICA")
        cat2 = database.CategoriaDB(nombre="HOGAR")
        cat3 = database.CategoriaDB(nombre="OFICINA")

        db.add(cat1)
        db.add(cat2)
        db.add(cat3)
        
        # Hacemos commit para que SQLite asigne los IDs
        db.commit()
        db.refresh(cat1)
        db.refresh(cat2)
        db.refresh(cat3)
        print("✅ Categorías creadas.")

        # 3. Crear Productos usando los IDs recién generados
        productos = [
            database.ProductoDB(nombre="LAPTOP GAMER", precio=1500.0, stock=10, categoria_id=cat1.id),
            database.ProductoDB(nombre="TECLADO RGB", precio=50.0, stock=25, categoria_id=cat1.id),
            database.ProductoDB(nombre="ESCRITORIO MADERA", precio=120.0, stock=5, categoria_id=cat3.id),
            database.ProductoDB(nombre="SILLA PRO", precio=250.0, stock=8, categoria_id=cat3.id),
            database.ProductoDB(nombre="SARTÉN ANTIADHERENTE", precio=35.0, stock=15, categoria_id=cat2.id),
        ]

        db.add_all(productos)
        db.commit()
        print(f"✅ {len(productos)} productos sembrados con éxito.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al cargar datos: {e}")
    finally:
        db.close()
        print("--- Proceso finalizado ---")

if __name__ == "__main__":
    cargar_datos_prueba()