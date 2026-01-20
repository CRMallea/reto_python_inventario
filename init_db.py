import database
from auth import get_password_hash

def inicializar_base_de_datos():
    # Crear tablas
    database.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()

    try:
        # 1. Crear Usuario Admin
        if not db.query(database.UsuarioDB).filter(database.UsuarioDB.username == "admin").first():
            admin = database.UsuarioDB(
                username="admin", 
                password_hash=get_password_hash("admin123")
            )
            db.add(admin)

        # 2. Crear Categorías
        categorias = ["Almacén", "Bebidas", "Limpieza", "Lácteos"]
        for cat_nombre in categorias:
            if not db.query(database.CategoriaDB).filter(database.CategoriaDB.nombre == cat_nombre).first():
                nueva_cat = database.CategoriaDB(nombre=cat_nombre)
                db.add(nueva_cat)
        db.commit()

        # 3. Crear Productos con diferentes niveles de stock para simular estados
        # (Nombre, Precio, Stock, ID_Categoría)
        productos_retail = [
            ("Aceite de Girasol 1.5L", 1200.50, 4, 1),   # ⚠️ REPOSICIÓN (Bajo stock)
            ("Arroz Largo Fino 1kg", 850.00, 45, 1),     # ✅ OK
            ("Fideos Tallarín 500g", 720.00, 3, 1),      # ⚠️ REPOSICIÓN
            ("Coca Cola 2.25L", 1500.00, 12, 2),         # ✅ OK
            ("Cerveza Quilmes 1L", 1100.00, 2, 2),       # ⚠️ REPOSICIÓN
            ("Detergente Lavavajilla", 950.00, 20, 3),   # ✅ OK
            ("Lavandina 1L", 600.00, 5, 3),              # ⚠️ REPOSICIÓN
            ("Leche Entera Larga Vida", 1100.00, 60, 4), # ✅ OK
            ("Yogur Frutilla 1kg", 1300.00, 8, 4),       # ✅ OK
            ("Jabón en Polvo 800g", 1800.00, 1, 3)       # ⚠️ REPOSICIÓN
        ]

        for nombre, precio, stock, cat_id in productos_retail:
            nuevo_prod = database.ProductoDB(
                nombre=nombre, 
                precio=precio, 
                stock=stock, 
                categoria_id=cat_id,
                descripcion="Producto de consumo masivo"
            )
            db.add(nuevo_prod)
        
        db.commit()
        print("✅ Base de datos reiniciada con éxito con productos de Retail.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inicializar_base_de_datos()