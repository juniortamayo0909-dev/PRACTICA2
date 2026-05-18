import streamlit as st
import pandas as pd
import requests
import time
from streamlit_lottie import st_lottie
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# CONFIGURACIÓN
st.set_page_config(
    page_title="🎮 Machine Learning Games",
    page_icon="🎮",
    layout="wide"
)

# ESTILOS CSS
st.markdown("""
<style>

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
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #9333ea, #ec4899);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# FUNCIÓN ANIMACIÓN
def load_lottie(url):

    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.json()

# ANIMACIÓN
animation = load_lottie(
    "https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

st_lottie(animation, height=300)

# TÍTULO
st.title("🎮 Clasificador de Juegos con Machine Learning")

st.markdown("""
<h3>Predicción de videojuegos más vendidos</h3>
""", unsafe_allow_html=True)

# CARGAR DATASET
@st.cache_data
def load_data():

    return pd.read_csv("vgsales.csv")

df = load_data()

# LIMPIAR COLUMNAS
df.columns = df.columns.str.strip().str.lower()

# ELIMINAR NULOS
df = df.dropna()

# ENCODERS
le_platform = LabelEncoder()
le_genre = LabelEncoder()
le_publisher = LabelEncoder()

# TRANSFORMACIÓN
df['platform_encoded'] = le_platform.fit_transform(df['platform'])

df['genre_encoded'] = le_genre.fit_transform(df['genre'])

df['publisher_encoded'] = le_publisher.fit_transform(df['publisher'])

# VARIABLE OBJETIVO
df['hit_game'] = df['global_sales'].apply(
    lambda x: 1 if x >= 1 else 0
)

# FEATURES
X = df[
    [
        'platform_encoded',
        'genre_encoded',
        'publisher_encoded',
        'na_sales',
        'eu_sales',
        'jp_sales',
        'other_sales'
    ]
]

y = df['hit_game']

# DIVISIÓN
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# MODELO
model = RandomForestClassifier()

model.fit(X_train, y_train)

# SIDEBAR
with st.sidebar:

    st.header("📊 Información")

    st.write(f"🎮 Juegos: {len(df)}")

    st.write(f"🕹 Plataformas: {df['platform'].nunique()}")

    st.write(f"🎲 Géneros: {df['genre'].nunique()}")

# INPUTS
platform = st.selectbox(
    "🕹 Plataforma",
    sorted(df['platform'].unique())
)

genre = st.selectbox(
    "🎲 Género",
    sorted(df['genre'].unique())
)

publisher = st.selectbox(
    "🏢 Publisher",
    sorted(df['publisher'].unique())
)

na_sales = st.number_input(
    "🇺🇸 NA Sales",
    min_value=0.0
)

eu_sales = st.number_input(
    "🇪🇺 EU Sales",
    min_value=0.0
)

jp_sales = st.number_input(
    "🇯🇵 JP Sales",
    min_value=0.0
)

other_sales = st.number_input(
    "🌎 Other Sales",
    min_value=0.0
)

# BOTÓN
if st.button("🚀 Predecir Juego"):

    with st.spinner("Analizando datos..."):
        time.sleep(1)

    # ENCODE
    platform_encoded = le_platform.transform(
        [platform]
    )[0]

    genre_encoded = le_genre.transform(
        [genre]
    )[0]

    publisher_encoded = le_publisher.transform(
        [publisher]
    )[0]

    # PREDICCIÓN
    prediction = model.predict([
        [
            platform_encoded,
            genre_encoded,
            publisher_encoded,
            na_sales,
            eu_sales,
            jp_sales,
            other_sales
        ]
    ])

    # RESULTADO
    if prediction[0] == 1:

        st.success(
            "🔥 El modelo predice que el juego será MUY VENDIDO"
        )

    else:

        st.error(
            "❌ El modelo predice que el juego NO será muy vendido"
        )

# TOP 10
st.markdown("---")

st.subheader("🏆 Top 10 Juegos Más Vendidos")

top10 = df.sort_values(
    by='global_sales',
    ascending=False
).head(10)

st.dataframe(
    top10[
        [
            'name',
            'platform',
            'genre',
            'publisher',
            'global_sales'
        ]
    ]
)

# DATASET
st.markdown("---")

st.subheader("📋 Dataset Completo")

if st.checkbox("Mostrar dataset"):

    st.dataframe(df)

# MÉTRICAS
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🎮 Juegos",
        len(df)
    )

with col2:

    st.metric(
        "🕹 Plataformas",
        df['platform'].nunique()
    )

with col3:

    st.metric(
        "🎲 Géneros",
        df['genre'].nunique()
    )

# CARACTERÍSTICAS
st.markdown("---")

st.markdown("""
## 🚀 Características

✅ Machine Learning  
✅ Random Forest Classifier  
✅ Predicción automática  
✅ Diseño gamer moderno  
✅ Animaciones interactivas  
✅ Dataset interactivo  
✅ Compatible con Streamlit Cloud  
""")

# GOOGLE COLAB
st.markdown("---")

st.subheader("📘 Google Colab")

st.write(
    "Entrenamiento y desarrollo completo del proyecto"
)

st.link_button(
    "🚀 Abrir Google Colab",
    "https://colab.research.google.com/drive/1OT7LM7ArkOZlrAyFH9CYhoLjwSRjCVhf?usp=sharing"
)
