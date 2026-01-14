import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Gestor de Inventario", layout="wide")

# Inicializar el estado del token
if "token" not in st.session_state:
    st.session_state.token = None

# --- LÓGICA DE INTERFAZ ---
st.title("📦 Sistema de Gestión de Inventario")

# 1. VISTA DE LOGIN
if st.session_state.token is None:
    st.subheader("🔐 Iniciar Sesión")
    with st.container():
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Entrar", use_container_width=True):
            try:
                resp = requests.post(
                    f"{API_URL}/usuarios/token", 
                    data={"username": user, "password": password}
                )
                if resp.status_code == 200:
                    st.session_state.token = resp.json()["access_token"]
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
            except Exception as e:
                st.error(f"No se pudo conectar con el servidor: {e}")

# 2. VISTA DASHBOARD (SOLO SI ESTÁ AUTENTICADO)
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    with st.sidebar:
        st.write(f"Conectado como: Administrador")
        if st.button("Cerrar Sesión"):
            st.session_state.token = None
            st.rerun()

    # --- SECCIÓN: LISTADO DE PRODUCTOS ---
    st.subheader("📋 Productos en Inventario")
    try:
        res = requests.get(f"{API_URL}/productos/", headers=headers)
        if res.status_code == 200:
            productos = res.json()
            if productos:
                df = pd.DataFrame(productos)
                
                # Manejo seguro de columnas para evitar "['descripcion'] not in index"
                columnas_posibles = ["nombre", "precio", "stock", "descripcion"]
                columnas_a_mostrar = [c for c in columnas_posibles if c in df.columns]
                
                st.dataframe(df[columnas_a_mostrar], use_container_width=True)
            else:
                st.info("No hay productos registrados todavía.")
        elif res.status_code == 401:
            st.error("Tu sesión ha expirado. Por favor, cierra sesión e inicia de nuevo.")
    except Exception as e:
        st.error(f"Error al cargar la lista: {e}")

    st.divider()

    # --- SECCIÓN: AÑADIR PRODUCTO ---
    st.subheader("➕ Registrar Nuevo Producto")
    with st.form("form_nuevo_producto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del Producto")
            precio = st.number_input("Precio de Venta", min_value=0.0, step=0.01)
            cat_id = st.number_input("ID de Categoría", min_value=1, value=1)
            
        with col2:
            stock = st.number_input("Cantidad en Stock", min_value=0, step=1)
            descripcion = st.text_area("Descripción (Opcional)")
            
        submitted = st.form_submit_button("Guardar Producto", use_container_width=True)

    if submitted:
        if not nombre:
            st.warning("El nombre del producto es obligatorio.")
        else:
            payload = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria_id": cat_id
            }
            try:
                # Usamos los 'headers' definidos al inicio del bloque else
                r = requests.post(f"{API_URL}/productos/", json=payload, headers=headers)
                
                if r.status_code in [200, 201]:
                    st.success(f"✅ Producto '{nombre.upper()}' guardado correctamente.")
                    st.rerun()
                else:
                    error_detail = r.json().get('detail', 'Error desconocido')
                    st.error(f"Error {r.status_code}: {error_detail}")
            except Exception as e:
                st.error(f"Fallo al intentar guardar: {e}")