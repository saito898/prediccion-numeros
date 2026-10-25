
import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import os
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="La Escuela de los Números",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# ESTÉTICA: AULA ESCOLAR
# --------------------------------------------------

st.markdown("""
<style>

/* Fondo de aula */
.stApp {
    background-color: #F5F0E5;
    color: #34443A;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Tipografía */
html, body, [class*="css"] {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}

h1, h2, h3 {
    color: #294638 !important;
}

p, label, .stMarkdown {
    color: #48584C;
}

/* Encabezado */
.school-header {
    background: #FFFDF7;
    border: 2px solid #D9CEB8;
    border-bottom: 7px solid #B68B58;
    border-radius: 15px;
    padding: 1.7rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 5px 0 rgba(115, 91, 57, 0.06);
}

.school-icon {
    font-size: 2.7rem;
    margin-bottom: 0.3rem;
}

.school-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #294638;
    letter-spacing: -1px;
    margin: 0;
}

.school-subtitle {
    font-size: 1rem;
    color: #7B806C;
    margin-top: 0.6rem;
}

.school-label {
    display: inline-block;
    margin-top: 1rem;
    background: #E7EEDB;
    color: #436246;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1.5px;
}

/* Títulos de las secciones */
.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #294638;
    margin-bottom: 0.3rem;
}

.section-caption {
    color: #7B806C;
    font-size: 0.94rem;
    margin-bottom: 1rem;
}

/* Tarjetas */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFDF7;
    border: 1px solid #DED4C1;
    border-radius: 15px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #E8E0CE;
    border-right: 2px solid #D2C4AB;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #294638 !important;
}

/* Tablero de tiza: marco exterior */
.chalkboard-frame {
    background: #A8794B;
    padding: 12px;
    border: 3px solid #825A36;
    border-radius: 9px;
    box-shadow:
        0 7px 0 #D7C3A2,
        0 10px 18px rgba(74, 55, 34, 0.13);
    margin-bottom: 1.3rem;
}

.chalkboard-label {
    color: #FFF8DF;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-align: center;
    padding: 5px 0 10px 0;
}

/* Canvas */
[data-testid="stCanvas"] {
    border: 2px solid #D4C29F;
    border-radius: 4px;
    overflow: hidden;
}

/* Filetes y separadores */
hr {
    border: none;
    border-top: 2px dashed #D7CBB5;
    margin: 1.6rem 0;
}

/* Botones */
.stButton > button {
    border-radius: 9px;
    min-height: 45px;
    font-weight: 750;
    border: 1px solid #A5B89B;
    background: #E7EEDB;
    color: #35533D;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #D6E4C8;
    border-color: #668663;
    color: #294638;
    transform: translateY(-1px);
}

/* Botón principal */
.stButton > button[kind="primary"] {
    background: #3E684C;
    color: #FFFFFF;
    border: 1px solid #31543C;
}

.stButton > button[kind="primary"]:hover {
    background: #31543C;
    color: #FFFFFF;
}

/* Métricas */
[data-testid="stMetric"] {
    background: #FFFDF7;
    border: 1px solid #DED4C1;
    border-top: 4px solid #7B9B6A;
    border-radius: 12px;
    padding: 1rem;
}

[data-testid="stMetricLabel"] {
    color: #77816E !important;
}

[data-testid="stMetricValue"] {
    color: #294638 !important;
}

/* Imágenes de procesamiento */
[data-testid="stImage"] img {
    border-radius: 10px;
    border: 2px solid #DED4C1;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #FFFDF7;
    border: 1px solid #DED4C1;
    border-radius: 10px;
}

/* Alertas */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Gráfico */
[data-testid="stVegaLiteChart"] {
    background: #FFFDF7;
    border: 1px solid #DED4C1;
    border-radius: 12px;
    padding: 0.5rem;
}

/* Pie de página */
.school-footer {
    margin-top: 3rem;
    text-align: center;
    color: #8A8978;
    font-size: 0.83rem;
    padding: 1.2rem;
    border-top: 2px dashed #D7CBB5;
}

.school-footer strong {
    color: #436246;
}

/* Pantallas pequeñas */
@media (max-width: 700px) {
    .school-title {
        font-size: 1.8rem;
    }

    .school-header {
        padding: 1.3rem 1rem;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ENCABEZADO ESCOLAR
# --------------------------------------------------

st.markdown("""
<div class="school-header">
    <div class="school-icon">📚 ✏️ 🧮</div>
    <div class="school-title">La Escuela de los Números</div>
    <div class="school-subtitle">
        ¡Escribe un número en el tablero y descubre qué aprendió nuestra IA!
    </div>
    <div class="school-label">AULA DIGITAL · MATEMÁTICAS</div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INFORMACIÓN TÉCNICA EN LA BARRA LATERAL
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🏫 Aula de tecnología")
    st.markdown("---")

    st.markdown("### 📖 Información del modelo")
    st.write(f"**TensorFlow:** `{tf.__version__}`")
    st.write(f"**Keras:** `{keras.__version__}`")

    st.markdown("---")
    st.markdown("### 📝 ¿Cómo jugar?")
    st.markdown("""
    1. Toma la tiza virtual.
    2. Dibuja un número del **0 al 9**.
    3. Pulsa **Predecir**.
    4. Descubre qué número reconoce la inteligencia artificial.
    5. ¡Borra el tablero y prueba otro!
    """)

    st.markdown("---")
    st.caption("Laboratorio de aprendizaje automático · MNIST")


# --------------------------------------------------
# CARGAR MODELO
# --------------------------------------------------

@st.cache_resource
def load_mnist_model():
    """Carga el modelo MNIST desde archivo .keras"""

    model_files = ["mnist_model.keras", "mnist_model.h5"]

    for model_path in model_files:
        if os.path.exists(model_path):
            try:
                st.info(f"📂 Intentando cargar: {model_path}")
                model = keras.models.load_model(model_path)
                st.success(
                    f"✅ Modelo cargado exitosamente desde: `{model_path}`"
                )
                return model

            except Exception as e:
                st.error(f"❌ Error al cargar {model_path}: {str(e)}")
                continue

    st.error("❌ No se encontró ningún modelo")
    st.info("""
    **Instrucciones:**
    1. Entrena el modelo en Google Colab.
    2. Descarga `mnist_model.keras`.
    3. Súbelo a la raíz de tu repositorio.
    4. Reinicia la aplicación.
    """)
    st.stop()


model = load_mnist_model()


# --------------------------------------------------
# TABLERO Y CONTROLES
# --------------------------------------------------

st.markdown("""
<div class="section-title">✏️ ¡Tu turno de escribir!</div>
<div class="section-caption">
    Dibuja un solo dígito del 0 al 9, como si estuvieras escribiendo en clase.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.7, 1], gap="large")

with col1:
    st.markdown("""
    <div class="chalkboard-frame">
        <div class="chalkboard-label">
            ✦ TABLERO DE TIZA · ESCRIBE AQUÍ ✦
        </div>
    </div>
    """, unsafe_allow_html=True)

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=20,
        stroke_color="#FFFFFF",
        background_color="#244B3B",
        width=400,
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )

    st.caption("🖍️ Usa el ratón o el dedo para escribir tu número.")

with col2:
    st.markdown("""
    <div class="section-title">🎒 Tu escritorio</div>
    <div class="section-caption">
        Cuando termines de escribir, pídele al modelo que adivine.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔎 ¿Qué número escribiste?")

    predict_btn = st.button(
        "🔍 Predecir número",
        type="primary",
        use_container_width=True
    )

    clear_btn = st.button(
        "🧽 Borrar tablero",
        use_container_width=True
    )

    if clear_btn:
        st.rerun()

    st.markdown("---")

    st.markdown("#### 💡 Consejo de la profe")
    st.info(
        "Escribe el número grande, centrado y con un trazo claro. "
        "¡Así será más fácil reconocerlo!"
    )

    st.markdown("""
    <div style="
        background:#F2E6C9;
        border-left:5px solid #C79A55;
        padding:14px;
        border-radius:8px;
        color:#675333;
        font-size:0.9rem;
    ">
        <strong>⭐ Reto del día</strong><br>
        ¿Cuántos números diferentes puedes escribir correctamente?
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# PREDICCIÓN
# --------------------------------------------------

if predict_btn:
    if canvas_result.image_data is not None:

        if np.max(canvas_result.image_data) == 0:
            st.warning("⚠️ ¡El tablero está vacío! Dibuja un número primero.")

        else:
            with st.spinner("🧠 La inteligencia artificial está pensando..."):

                # Procesar imagen
                image = Image.fromarray(
                    canvas_result.image_data.astype("uint8")
                ).convert("L")

                image_resized = image.resize(
                    (28, 28),
                    Image.Resampling.LANCZOS
                )

                img_array = np.array(image_resized) / 255.0
                img_array = img_array.reshape(1, 28, 28, 1)

                # Predicción
                prediction = model.predict(img_array, verbose=0)
                digit = np.argmax(prediction)
                confidence = np.max(prediction) * 100

            # ------------------------------------------
            # RESULTADO PRINCIPAL
            # ------------------------------------------

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""
            <div class="section-title">🏆 ¡Tenemos una respuesta!</div>
            <div class="section-caption">
                La profesora virtual ha revisado tu escritura.
            </div>
            """, unsafe_allow_html=True)

            st.success(f"## 🎯 ¡El dígito detectado es: {digit}!")

            col_m1, col_m2, col_m3 = st.columns(3)

            with col_m1:
                st.metric("📘 Predicción", digit)

            with col_m2:
                st.metric("🎯 Confianza", f"{confidence:.1f}%")

            with col_m3:
                alternative = np.argsort(prediction[0])[-2]
                st.metric("🔢 Segunda opción", alternative)

            # ------------------------------------------
            # PROCESAMIENTO DE IMAGEN
            # ------------------------------------------

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""
            <div class="section-title">🔬 Así ve la IA tu número</div>
            <div class="section-caption">
                La imagen original se transforma en una cuadrícula de 28 × 28 píxeles.
            </div>
            """, unsafe_allow_html=True)

            col_img1, col_img2 = st.columns(2)

            with col_img1:
                st.markdown("#### ✏️ Tu dibujo original")
                st.image(
                    canvas_result.image_data,
                    width=250
                )

            with col_img2:
                st.markdown("#### 🧩 Imagen procesada")
                st.image(
                    image_resized,
                    width=250
                )

            # ------------------------------------------
            # PROBABILIDADES
            # ------------------------------------------

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""
            <div class="section-title">📊 Las respuestas posibles</div>
            <div class="section-caption">
                Observa qué probabilidad le asigna el modelo a cada dígito.
            </div>
            """, unsafe_allow_html=True)

            prob_df = pd.DataFrame({
                "Dígito": [str(i) for i in range(10)],
                "Probabilidad (%)": prediction[0] * 100
            })

            st.bar_chart(prob_df.set_index("Dígito"))

            with st.expander("🔍 Ver las calificaciones de todos los números"):
                for i, prob in enumerate(prediction[0]):
                    emoji = "🏆" if i == digit else "✏️"
                    st.write(
                        f"{emoji} **Dígito {i}:** {prob * 100:.2f}%"
                    )

    else:
        st.warning("⚠️ ¡Dibuja un número en el tablero antes de predecir!")


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
<div class="school-footer">
    <strong>🏫 La Escuela de los Números</strong><br>
    Aprender, experimentar y descubrir con inteligencia artificial.<br>
    <span style="font-size:0.75rem;">
        Powered by TensorFlow · Keras · MNIST
    </span>
</div>
""", unsafe_allow_html=True)
