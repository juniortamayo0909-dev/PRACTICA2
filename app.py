
import streamlit as st
import pandas as pd
import pickle
from streamlit_lottie import st_lottie
import requests

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Clasificador de Juegos",
    page_icon="🎮",
    layout="wide"
)

# ESTILOS CSS
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

h1 {
    color: white;
    text-align: center;
}

.stButton>button {
    background-color: #9333ea;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0px 0px 10px rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# FUNCIÓN PARA ANIMACIÓN LOTTIE

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_game = load_lottie("https://assets2.lottiefiles.com/packages/lf20_x62chJ.json")

# ANIMACIÓN
st_lottie(lottie_game, height=250)

# TÍTULO
st.title("🎮 Clasificador de Juegos Más Vendidos")

# CARGAR DATASET
@st.cache_data

def load_data():
    return pd.read_csv("vgsales.csv")


df = load_data()

# INPUT DEL USUARIO
juego = st.text_input("Ingrese el nombre del juego")

# BOTÓN
if st.button("Buscar Juego"):

    resultado = df[df['Name'].str.contains(juego, case=False, na=False)]

    if not resultado.empty:
        fila = resultado.iloc[0]

        st.success("Juego encontrado")

        st.markdown(f"""
        <div class='card'>
        <h2>{fila['Name']}</h2>
        <p><b>Rank:</b> {fila['Rank']}</p>
        <p><b>Platform:</b> {fila['Platform']}</p>
        <p><b>Year:</b> {fila['Year']}</p>
        <p><b>Genre:</b> {fila['Genre']}</p>
        <p><b>Publisher:</b> {fila['Publisher']}</p>
        <p><b>NA Sales:</b> {fila['NA_Sales']}</p>
        <p><b>EU Sales:</b> {fila['EU_Sales']}</p>
        <p><b>JP Sales:</b> {fila['JP_Sales']}</p>
        <p><b>Other Sales:</b> {fila['Other_Sales']}</p>
        <p><b>Global Sales:</b> {fila['Global_Sales']}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("Juego no encontrado")
```

---

# requirements.txt

```txt
streamlit
pandas
scikit-learn
streamlit-lottie
requests
```

---

# Cómo subirlo a GitHub y Streamlit

## 1. Crear repositorio en GitHub

Sube los archivos:

* app.py
* vgsales.csv
* requirements.txt
* modelo.pkl
* encoder.pkl

---

## 2. Ir a Streamlit Cloud

Página oficial:

[https://streamlit.io/cloud](https://streamlit.io/cloud)

---

## 3. Conectar GitHub

* Inicia sesión
* Selecciona el repositorio
* Escoge app.py
* Deploy

---

## Google Colab del Proyecto

Puedes acceder al entrenamiento y desarrollo del modelo en el siguiente enlace:

st.markdown("[Abrir Google Colab](https://colab.research.google.com/drive/1OT7LM7ArkOZlrAyFH9CYhoLjwSRjCVhf?usp=sharing)")

---

## Resultado

La página tendrá:

✅ Buscador de juegos
✅ Datos completos del videojuego
✅ Diseño moderno
✅ Animaciones
✅ Compatible con GitHub y Streamlit Cloud
