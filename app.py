import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

from streamlit_lottie import st_lottie

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="🎮 ML Games Dashboard",
    page_icon="🎮",
    layout="wide"
)

# =========================================================
# CSS GAMER
# =========================================================

st.markdown("""
<style>

body {
    background-color: #020617;
}

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
    color: white;
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    transition: 0.3s;
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0px 0px 25px #9333ea;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(
        to right,
        #9333ea,
        #ec4899
    );
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
    border: none;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOTTIE
# =========================================================

def load_lottie(url):

    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.json()

gaming_animation = load_lottie(
    "https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

success_animation = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json"
)

# =========================================================
# HEADER
# =========================================================

st_lottie(
    gaming_animation,
    height=300
)

st.title("🎮 Machine Learning Games Dashboard")

st.markdown("""
<h3>
Predicción Inteligente de Videojuegos Exitosos
</h3>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("vgsales.csv")

    return df

df = load_data()

# =========================================================
# CLEAN DATA
# =========================================================

df.columns = df.columns.str.strip().str.lower()

df['year'] = pd.to_numeric(
    df['year'],
    errors='coerce'
)

df = df.dropna()

# =========================================================
# LABEL ENCODERS
# =========================================================

le_platform = LabelEncoder()
le_genre = LabelEncoder()
le_publisher = LabelEncoder()

df['platform_encoded'] = le_platform.fit_transform(
    df['platform']
)

df['genre_encoded'] = le_genre.fit_transform(
    df['genre']
)

df['publisher_encoded'] = le_publisher.fit_transform(
    df['publisher']
)

# =========================================================
# TARGET
# =========================================================

df['hit_game'] = df['global_sales'].apply(
    lambda x: 1 if x >= 1 else 0
)

# =========================================================
# FEATURES
# =========================================================

X = df[
    [
        'platform_encoded',
        'genre_encoded',
        'publisher_encoded',
        'year'
    ]
]

y = df['hit_game']

# =========================================================
# SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================================================
# MODEL
# =========================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# =========================================================
# ACCURACY
# =========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/686/686589.png",
        width=120
    )

    st.title("🎮 ML Games")

    st.markdown("---")

    st.metric(
        "🎮 Juegos",
        len(df)
    )

    st.metric(
        "🕹 Plataformas",
        df['platform'].nunique()
    )

    st.metric(
        "🎲 Géneros",
        df['genre'].nunique()
    )

    st.metric(
        "🎯 Accuracy",
        f"{accuracy:.2%}"
    )

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🎮 Predicción",
    "📊 Estadísticas",
    "🏆 Rankings",
    "📋 Dataset"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown("## 🎯 Predicción Inteligente")

    col1, col2 = st.columns(2)

    with col1:

        platform = st.selectbox(
            "🕹 Plataforma",
            sorted(df['platform'].unique())
        )

        genre = st.selectbox(
            "🎲 Género",
            sorted(df['genre'].unique())
        )

    with col2:

        publisher = st.selectbox(
            "🏢 Publisher",
            sorted(df['publisher'].unique())
        )

        year = st.slider(
            "📅 Año",
            1980,
            2025,
            2015
        )

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

    # BUTTON
    if st.button("🚀 Analizar Juego"):

        with st.spinner(
            "🧠 La IA está analizando el videojuego..."
        ):
            time.sleep(2)

        input_data = pd.DataFrame([{
            'platform_encoded': platform_encoded,
            'genre_encoded': genre_encoded,
            'publisher_encoded': publisher_encoded,
            'year': year
        }])

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]

        st.markdown("---")

        st.markdown("## 🎯 Resultado")

        st.progress(
            float(probability)
        )

        st.markdown(f"""
        <div class="card">
            <h1 style="text-align:center;">
                {probability:.2%}
            </h1>
            <p style="text-align:center;">
                Probabilidad de Éxito
            </p>
        </div>
        """, unsafe_allow_html=True)

        if probability >= 0.8:

            st.success(
                "🔥 HIT MUNDIAL DETECTADO"
            )

            st.balloons()

            st_lottie(
                success_animation,
                height=250
            )

            st.info("""
            📈 El modelo detectó patrones similares
            a videojuegos extremadamente exitosos.
            """)

        elif probability >= 0.5:

            st.warning(
                "⚡ Buen potencial comercial"
            )

            st.info("""
            🎮 El juego tiene posibilidades
            interesantes en el mercado.
            """)

        else:

            st.error(
                "❌ Riesgo de bajas ventas"
            )

            st.info("""
            📉 El modelo detecta patrones
            asociados a juegos con ventas bajas.
            """)

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown("## 📊 Estadísticas Interactivas")

    # SALES BY GENRE
    genre_sales = df.groupby(
        'genre'
    )['global_sales'].sum().reset_index()

    fig1 = px.bar(
        genre_sales,
        x='genre',
        y='global_sales',
        color='global_sales',
        title='🎮 Ventas por Género',
        template='plotly_dark'
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # PLATFORM SALES
    platform_sales = df.groupby(
        'platform'
    )['global_sales'].sum().reset_index()

    fig2 = px.pie(
        platform_sales,
        names='platform',
        values='global_sales',
        title='🕹 Distribución por Plataforma',
        template='plotly_dark'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # FEATURE IMPORTANCE
    importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    })

    fig3 = px.bar(
        importance,
        x='Feature',
        y='Importance',
        color='Importance',
        title='🧠 Importancia de Variables',
        template='plotly_dark'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.markdown("## 🏆 Ranking de Juegos")

    top_n = st.slider(
        "🎮 Selecciona Top",
        5,
        50,
        10
    )

    top_games = df.sort_values(
        by='global_sales',
        ascending=False
    ).head(top_n)

    st.dataframe(
        top_games[
            [
                'name',
                'platform',
                'genre',
                'publisher',
                'global_sales'
            ]
        ],
        use_container_width=True
    )

    # SEARCH
    st.markdown("---")

    search = st.text_input(
        "🔎 Buscar Juego"
    )

    filtered = df[
        df['name'].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered[
            [
                'name',
                'platform',
                'genre',
                'publisher',
                'global_sales'
            ]
        ],
        use_container_width=True
    )

# =========================================================
# TAB 4
# =========================================================

with tab4:

    st.markdown("## 📋 Dataset Completo")

    if st.checkbox("Mostrar Dataset"):

        st.dataframe(
            df,
            use_container_width=True
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;">

<h3>🚀 Características</h3>

✅ Machine Learning  
✅ Random Forest  
✅ Dashboard Gamer  
✅ Plotly Interactive  
✅ Streamlit Cloud Ready  
✅ Predicción Inteligente  
✅ Diseño Responsive  
✅ Animaciones Gamer  

</div>
""", unsafe_allow_html=True)

# =========================================================
# COLAB
# =========================================================

st.markdown("---")

st.subheader("📘 Google Colab")

st.link_button(
    "🚀 Abrir Google Colab",
    "https://colab.research.google.com/drive/1OT7LM7ArkOZlrAyFH9CYhoLjwSRjCVhf?usp=sharing"
)
