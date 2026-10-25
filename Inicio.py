
import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import os

st.set_page_config(
    page_title="La Escuela de los Números",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# ESTILO VISUAL: AULA ESCOLAR
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Nunito:wght@400;500;600;700;800;900&display=swap');

:root {
    --wall: #f3ead8;
    --paper: #fffaf0;
    --wood: #a86636;
    --wood-dark: #714324;
    --green: #173e32;
    --green-light: #285847;
    --chalk: #f6f1dc;
    --yellow: #f3ce68;
    --ink: #263d35;
}

/* Fondo general */
.stApp {
    background:
        radial-gradient(ellipse at 50% 0%, #fff9ed 0%, transparent 60%),
        linear-gradient(180deg, #eee1cb 0%, #f8f1e4 68%, #e3c8a3 100%);
    color: var(--ink);
    font-family: 'Nunito', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Ocultar elementos decorativos predeterminados */
#MainMenu, footer {
    visibility: hidden;
}

/* Encabezado como una gran pizarra */
.classroom-board {
    position: relative;
    background:
        radial-gradient(ellipse at 20% 30%, rgba(255,255,255,.035), transparent 45%),
        repeating-linear-gradient(3deg, transparent 0px, rgba(255,255,255,.018) 2px, transparent 5px),
        #173c30;
    border: 12px solid #9b6035;
    border-radius: 8px;
    box-shadow:
        inset 0 0 0 3px #c68d55,
        inset 0 0 35px rgba(0,0,0,.25),
        0 8px 0 #714324,
        0 13px 22px rgba(70,43,21,.25);
    padding: 24px 20px 26px;
    margin-bottom: 28px;
    text-align: center;
    color: #fff9e8;
}

.classroom-board:after {
    content: "✦  ✎  ✦";
    position: absolute;
    right: 22px;
    bottom: 8px;
    color: #e8d38b;
    font-size: 17px;
    letter-spacing: 8px;
}

.board-eyebrow {
    font-family: 'Nunito', sans-serif;
    text-transform: uppercase;
    letter-spacing: 4px;
    font-size: 11px;
    font-weight: 900;
    color: #e8cd76;
    margin-bottom: 5px;
}

.board-title {
    font-family: 'Patrick Hand', cursive;
    font-size: clamp(36px, 5vw, 62px);
    line-height: 1.05;
    color: #fff9e8;
    text-shadow: 1px 2px 0 rgba(0,0,0,.25);
    margin: 0;
}

.board-subtitle {
    font-family: 'Patrick Hand', cursive;
    font-size: 23px;
    color: #dce8d9;
    margin-top: 8px;
}

.board-chalk-line {
    width: 120px;
    height: 3px;
    margin: 14px auto 0;
    background: #e8cd76;
    border-radius: 3px;
}

/* Pequeños letreros */
.section-sign {
    background: #fff9ed;
    border: 2px solid #d9c4a4;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 0 rgba(113,67,36,.12);
    margin: 4px 0 15px;
    color: #29483b;
    font-weight: 900;
    font-size: 19px;
}

.section-sign small {
    display: block;
    color: #8b735a;
    font-size: 12px;
    font-weight: 700;
    margin-top: 3px;
}

/* Pizarra de instrucciones */
.side-blackboard {
    background:
        repeating-linear-gradient(0deg, transparent 0px, rgba(255,255,255,.015) 2px, transparent 4px),
        #193f33;
    color: #fff9e8;
    border: 7px solid #a66c3f;
    border-radius: 5px;
    padding: 20px 17px;
    box-shadow: inset 0 0 0 2px #c48a53, 0 6px 10px rgba(66,40,20,.13);
    margin-bottom: 17px;
}

.side-blackboard h3 {
    font-family: 'Patrick Hand', cursive;
    font-size: 25px;
    color: #f2d577;
    margin: 0 0 14px;
}

.side-blackboard p {
    color: #f7f1df;
    font-size: 14px;
    line-height: 1.6;
}

.side-blackboard hr {
    border: 0;
    border-top: 1px dashed #8ca79a;
    margin: 15px 0;
}

/* Tarjetas de papel */
.paper-card {
    background: rgba(255,250,240,.96);
    border: 1px solid #e2d0b4;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 5px 0 rgba(116,76,39,.10), 0 10px 24px rgba(87,57,28,.08);
    margin-bottom: 17px;
}

.paper-heading {
    font-size: 19px;
    font-weight: 900;
    color: #29483b;
    margin-bottom: 5px;
}

.paper-caption {
    font-size: 12px;
    color: #8c7a64;
    margin-bottom: 13px;
}

/* Área central del tablero */
.drawing-frame {
    background: linear-gradient(135deg, #c48a53, #86502c 40%, #c48a53 70%, #754323);
    padding: 10px;
    border-radius: 8px;
    box-shadow:
        inset 0 0 0 2px #e0b47d,
        0 6px 0 #714324,
        0 10px 18px rgba(65,39,18,.18);
    margin-bottom: 17px;
}

.drawing-label {
    font-family: 'Patrick Hand', cursive;
    color: #f7f0df;
    background: #173c30;
    text-align: center;
    padding: 7px;
    font-size: 17px;
    border-radius: 3px 3px 0 0;
}

/* Botones */
.stButton > button {
    border-radius: 10px;
    min-height: 46px;
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    border: 2px solid #d7c2a2;
    background: #fff9ed;
    color: #29483b;
    transition: all .18s ease;
    box-shadow: 0 3px 0 rgba(113,67,36,.13);
}

.stButton > button:hover {
    border-color: #a66c3f;
    color: #173e32;
    transform: translateY(-2px);
    box-shadow: 0 5px 0 rgba(113,67,36,.15);
}

.stButton > button[kind="primary"] {
    background: #245b48;
    color: #fff9ed;
    border-color: #194333;
}

.stButton > button[kind="primary"]:hover {
    background: #34765d;
    color: white;
}

/* Métricas */
[data-testid="stMetric"] {
    background: #fffaf0;
    border: 1px solid #e2d0b4;
    border-radius: 12px;
    padding: 13px;
    box-shadow: 0 3px 0 rgba(113,67,36,.08);
}

[data-testid="stMetricLabel"] {
    color: #78654f;
    font-weight: 800;
}

[data-testid="stMetricValue"] {
    color: #245b48;
    font-weight: 900;
}

/* Mensajes */
.stAlert {
    border-radius: 10px;
}

/* Gráficas y expanders */
[data-testid="stExpander"] {
    background: #fffaf0;
    border: 1px solid #e2d0b4;
    border-radius: 10px;
}

[data-testid="stImage"] img {
    border-radius: 8px;
}

/* Separadores */
hr {
    border-color: #ddc8a7;
}

/* Pie decorativo */
.classroom-footer {
    text-align: center;
    font-family: 'Patrick Hand', cursive;
    color: #75543a;
    font-size: 19px;
    margin-top: 22px;
    padding: 14px;
    border-top: 2px dashed #c4a57d;
}

@media (max-width: 800px) {
    .classroom-board {
        border-width: 7px;
        padding: 20px 10px;
    }

    .board-subtitle {
        font-size: 18px;
    }

    .side-blackboard {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO PRINCIPAL
# =========================================================

st.markdown("""
<div class="classroom-board">
    <div class="board-eyebrow">Aula de inteligencia artificial · Matemáticas</div>
    <h1 class="board-title">La Escuela de los Números</h1>
    <div class="board-subtitle">
        ¡Escribe con tiza y descubre qué número reconoce nuestra inteligencia artificial!
    </div>
    <div class="board-chalk-line"></div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INFORMACIÓN DEL MODELO
# =========================================================

with st.sidebar:
    st.markdown("""
    <div class="side-blackboard">
        <h3>📚 Rincón del conocimiento</h3>
        <p>Bienvenido al aula. Aquí aprenderemos cómo una inteligencia artificial reconoce los números escritos a mano.</p>
        <hr>
        <h3>🧑‍🏫 ¿Cómo participar?</h3>
        <p><b>1.</b> Dibuja un número del 0 al 9 en el tablero.</p>
        <p><b>2.</b> Pulsa el botón de predecir.</p>
        <p><b>3.</b> Observa qué número reconoce la IA.</p>
        <p><b>4.</b> Revisa su nivel de confianza y las otras posibilidades.</p>
        <hr>
        <p style="text-align:center;font-family:'Patrick Hand',cursive;font-size:20px;color:#f2d577;">
            ¡Cada trazo es una oportunidad para aprender!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔬 Ficha técnica del modelo")
    st.write(f"**TensorFlow:** `{tf.__version__}`")
    st.write(f"**Keras:** `{keras.__version__}`")
    st.caption("Modelo de clasificación entrenado con el conjunto de datos MNIST.")


# =========================================================
# CARGA DEL MODELO
# =========================================================

@st.cache_resource
def load_mnist_model():
    model_files = ["mnist_model.keras", "mnist_model.h5"]

    for model_path in model_files:
        if os.path.exists(model_path):
            try:
                model = keras.models.load_model(model_path)
                return model
            except Exception as e:
                st.error(f"Error al cargar {model_path}: {str(e)}")

    st.error("No se encontró ningún modelo compatible.")
    st.info("""
    **Para solucionarlo:**
    1. Entrena el modelo en Google Colab.
    2. Descarga `mnist_model.keras`.
    3. Sube el archivo a la raíz de tu repositorio.
    4. Reinicia la aplicación.
    """)
    st.stop()


model = load_mnist_model()


# =========================================================
# DISTRIBUCIÓN DEL AULA
# =========================================================

col_dibujo, col_resultados = st.columns([1.12, 0.88], gap="large")


# =========================================================
# ZONA DE DIBUJO
# =========================================================

with col_dibujo:
    st.markdown("""
    <div class="section-sign">
        ✏️ El tablero del estudiante
        <small>Escribe un solo número, del 0 al 9</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="drawing-label">✦ Pizarra de tiza ✦</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="drawing-frame">', unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("🖍️ Usa el ratón o el dedo para escribir en la pizarra.")

    btn_predecir, btn_limpiar = st.columns(2)

    with btn_predecir:
        predict_btn = st.button(
            "🔎 Predecir número",
            type="primary",
            use_container_width=True
        )

    with btn_limpiar:
        clear_btn = st.button(
            "🧽 Borrar pizarra",
            use_container_width=True
        )

    if clear_btn:
        st.rerun()

    st.markdown("""
    <div class="paper-card">
        <div class="paper-heading">💡 Consejo del profesor</div>
        <div class="paper-caption">
            Escribe el número grande, centrado y con un trazo claro.
            La IA puede confundirse si los números se parecen entre sí.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ZONA DE RESULTADOS
# =========================================================

with col_resultados:
    st.markdown("""
    <div class="section-sign">
        🧑‍🏫 Evaluación del profesor
        <small>Resultados del reconocimiento automático</small>
    </div>
    """, unsafe_allow_html=True)

    result_placeholder = st.empty()

    with result_placeholder.container():
        st.markdown("""
        <div class="paper-card" style="text-align:center;padding:35px 18px;">
            <div style="font-size:48px;">📋</div>
            <div class="paper-heading">Tu evaluación aparecerá aquí</div>
            <div class="paper-caption">
                Dibuja un número en el tablero y pulsa
                <b>Predecir número</b> para comenzar.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# PREDICCIÓN
# =========================================================

if predict_btn:
    if canvas_result.image_data is None:
        st.warning("Primero dibuja un número en el tablero.")
    else:
        # Convertir el dibujo a escala de grises y separar la tiza
        # blanca del fondo verde para mantener el formato de MNIST.
        rgba = canvas_result.image_data.astype("uint8")
        rgb = rgba[:, :, :3]

        # El trazo blanco destaca por su luminosidad.
        gray = np.array(
            Image.fromarray(rgb).convert("L")
        )

        # MNIST espera fondo negro y trazo blanco.
        # El umbral elimina el color de la pizarra y conserva la tiza.
        drawing_mask = gray > 145

        if not np.any(drawing_mask):
            st.warning("¡La pizarra está vacía! Dibuja un número antes de predecir.")
        else:
            with st.spinner("🔔 El profesor está revisando tu respuesta..."):
                processed = np.zeros_like(gray, dtype=np.uint8)
                processed[drawing_mask] = 255

                image = Image.fromarray(processed)
                image_resized = image.resize(
                    (28, 28),
                    Image.Resampling.LANCZOS
                )

                img_array = np.array(image_resized).astype("float32") / 255.0
                img_array = img_array.reshape(1, 28, 28, 1)

                prediction = model.predict(img_array, verbose=0)
                digit = int(np.argmax(prediction))
                confidence = float(np.max(prediction) * 100)
                alternative = int(np.argsort(prediction[0])[-2])

            with col_resultados:
                st.markdown(f"""
                <div class="paper-card" style="text-align:center;border-top:5px solid #3d8064;">
                    <div style="font-size:13px;color:#8b735a;font-weight:900;text-transform:uppercase;letter-spacing:2px;">
                        Resultado de la evaluación
                    </div>
                    <div style="font-size:65px;line-height:1.2;font-weight:900;color:#245b48;">
                        {digit}
                    </div>
                    <div style="font-size:16px;color:#3d8064;font-weight:900;">
                        ¡La IA cree que escribiste un {digit}!
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_m1, col_m2, col_m3 = st.columns(3)

                with col_m1:
                    st.metric("🎯 Predicción", digit)

                with col_m2:
                    st.metric("📈 Confianza", f"{confidence:.1f}%")

                with col_m3:
                    st.metric("📝 Alternativa", alternative)

                st.markdown("""
                <div class="paper-card">
                    <div class="paper-heading">🖼️ Cuaderno de procesamiento</div>
                    <div class="paper-caption">
                        Así se ve tu escritura antes y después de convertirse en una imagen de 28 × 28 píxeles.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_img1, col_img2 = st.columns(2)

                with col_img1:
                    st.markdown("**Tu dibujo**")
                    st.image(
                        rgba,
                        caption="Pizarra original",
                        width = 200
                    )

                with col_img2:
                    st.markdown("**Imagen para la IA**")
                    st.image(
                        image_resized,
                        caption="28 × 28 píxeles",
                        width = 200
                    )

                st.markdown("""
                <div class="paper-card">
                    <div class="paper-heading">📊 Calificaciones por número</div>
                    <div class="paper-caption">
                        La altura de cada barra indica la probabilidad que asigna el modelo a cada dígito.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                prob_df = pd.DataFrame({
                    "Dígito": [str(i) for i in range(10)],
                    "Probabilidad (%)": prediction[0] * 100
                })

                st.bar_chart(
                    prob_df.set_index("Dígito"),
                    use_container_width=True
                )

                with st.expander("📖 Ver el informe completo del profesor"):
                    for i, prob in enumerate(prediction[0]):
                        if i == digit:
                            st.write(f"🏆 **Dígito {i}: {prob * 100:.2f}%** — Predicción principal")
                        else:
                            st.write(f"✏️ Dígito {i}: {prob * 100:.2f}%")

                if confidence >= 90:
                    st.success("¡Excelente! La IA reconoce el número con mucha confianza.")
                elif confidence >= 65:
                    st.info("La IA tiene una buena idea, pero algunos números podrían parecerse.")
                else:
                    st.warning("La IA no está muy segura. Prueba a escribir el número más claramente.")


# =========================================================
# PIE DEL AULA
# =========================================================

st.markdown("""
<div class="classroom-footer">
    ✦ Aprender es descubrir algo nuevo cada día ✦
    <div style="font-family:'Nunito',sans-serif;font-size:11px;margin-top:5px;">
        Laboratorio escolar de inteligencia artificial · Modelo MNIST
    </div>
</div>
""", unsafe_allow_html=True)
