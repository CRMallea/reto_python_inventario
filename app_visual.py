import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Inventario Seguro", layout="wide")

API_URL = "http://127.0.0.1:8000"

# --- LÓGICA DE SESIÓN ---
if "token" not in st.session_state:
    st.session_state.token = None

# --- FUNCIÓN PARA LOGIN ---
def login(username, password):
    payload = {"username": username, "password": password}
    try:
        # FastAPI espera un formulario (data=), no un JSON (json=) para el token
        response = requests.post(f"{API_URL}/auth/token", data=payload)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except:
        return None

# --- PANTALLA DE LOGIN ---
if st.session_state.token is None:
    st.title("🔐 Acceso al Sistema")
    with st.form("login_form"):
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        boton = st.form_submit_button("Entrar")
        
        if boton:
            token = login(user, pw)
            if token:
                st.session_state.token = token
                st.success("¡Bienvenido!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    st.stop() # Detiene la ejecución aquí si no hay login

# --- SI LLEGAMOS AQUÍ, EL USUARIO ESTÁ AUTENTICADO ---
HEADERS = {"Authorization": f"Bearer {st.session_state.token}"}

st.sidebar.title("Navegación")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.token = None
    st.rerun()

menu = st.sidebar.selectbox("Ir a:", ["Ver Productos", "Añadir Producto"])

# --- VISTA: VER PRODUCTOS ---
if menu == "Ver Productos":
    st.title("📦 Inventario Actual")
    # Enviamos el TOKEN en los headers
    res = requests.get(f"{API_URL}/productos/", headers=HEADERS)
    
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            st.dataframe(df[['id', 'nombre', 'precio', 'stock']], use_container_width=True)
        else:
            st.info("No hay productos.")
    else:
        st.error("Tu sesión ha expirado. Por favor, vuelve a entrar.")
        st.session_state.token = None
