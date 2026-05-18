import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time

# CONFIGURACIÓN
st.set_page_config(
    page_title="🎮 Juegos Más Vendidos",
    page_icon="🎮",
    layout="wide"
)

# CSS Y ANIMACIONES
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

.card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 20px;
    color: white;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.15);
    animation: fadeIn 1s ease-in-out;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #9333ea, #ec4899);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# FUNCIÓN LOTTIE
def load_lottie(url):
    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.json()

# ANIMACIONES
gaming_animation = load_lottie(
    "https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

controller_animation = load_lottie(
    "https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json"
)

# ANIMACIÓN PRINCIPAL
st_lottie(gaming_animation, height=300)

# TÍTULO
st.title("🎮 Clasificador de Juegos Más Vendidos")

st.markdown("""
<h3>
Explora información de los videojuegos más vendidos del mundo
</h3>
""", unsafe_allow_html=True)

# CARGAR DATASET
@st.cache_data
def load_data():
    return pd.read_csv("vgsales.csv")

df = load_data()

# SIDEBAR
with st.sidebar:

    st_lottie(controller_animation, height=200)

    st.header("📊 Información")

    st.write(f"Cantidad de juegos: {len(df)}")

    st.write(f"Plataformas: {df['Platform'].nunique()}")

    st.write(f"Géneros: {df['Genre'].nunique()}")

# SELECTOR
juego = st.selectbox(
    "🎮 Seleccione un videojuego",
    sorted(df['Name'].unique())
)

# BOTÓN
if st.button("🔍 Buscar Información"):

    with st.spinner("Buscando juego..."):
        time.sleep(1)

    resultado = df[df['Name'] == juego]

    if not resultado.empty:

        fila = resultado.iloc[0]

        st.success("✅ Juego encontrado")

        st.markdown(f"""
        <div class="card">

        <h2>{fila['Name']}</h2>

        <hr>

        <h3>🎯 Información General</h3>

        <p><b>🏆 Rank:</b> {fila['Rank']}</p>

        <p><b>🕹 Plataforma:</b> {fila['Platform']}</p>

        <p><b>📅 Año:</b> {fila['Year']}</p>

        <p><b>🎲 Género:</b> {fila['Genre']}</p>

        <p><b>🏢 Publisher:</b> {fila['Publisher']}</p>

        <hr>

        <h3>💰 Ventas</h3>

        <p><b>🇺🇸 NA Sales:</b> {fila['NA_Sales']} millones</p>

        <p><b>🇪🇺 EU Sales:</b> {fila['EU_Sales']} millones</p>

        <p><b>🇯🇵 JP Sales:</b> {fila['JP_Sales']} millones</p>

        <p><b>🌎 Other Sales:</b> {fila['Other_Sales']} millones</p>

        <p><b>🔥 Global Sales:</b> {fila['Global_Sales']} millones</p>

        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("❌ Juego no encontrado")

# FOOTER
st.markdown("---")

st.markdown("""
## 🚀 Características

✅ Buscador inteligente  
✅ Diseño gamer moderno  
✅ Animaciones interactivas  
✅ Información completa  
✅ Compatible con Streamlit Cloud  
""")

# LINK COLAB
st.markdown("""
### 📘 Google Colab del Proyecto
""")

st.markdown(
    "[🔗 Abrir Google Colab](https://colab.research.google.com/drive/1OT7LM7ArkOZlrAyFH9CYhoLjwSRjCVhf?usp=sharing)"
)
