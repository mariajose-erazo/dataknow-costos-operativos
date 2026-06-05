"""
streamlit_app.py
----------------
Aplicación interactiva para visualización de resultados
y chat con el agente conversacional.

Ejecución:
    streamlit run app/streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent / "src"))

# ─────────────────────────────────────────
# Configuración de la página
# ─────────────────────────────────────────
st.set_page_config(
    page_title="DataKnow — Costos Operativos",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
st.sidebar.title("DataKnow")
st.sidebar.markdown("**Anticipación de Costos Operativos**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Análisis Exploratorio", "Proyecciones", "Agente IA"]
)

# ─────────────────────────────────────────
# Página: Inicio
# ─────────────────────────────────────────
if page == "Inicio":
    st.title("Anticipación de Costos Operativos")
    st.markdown("""
    Esta aplicación permite explorar los resultados del análisis de costos
    de **Equipo 1** y **Equipo 2**, proyectar costos futuros y consultar
    al agente de IA sobre los hallazgos del proyecto.

    ### ¿Qué puedes hacer aquí?
    - 📊 **Análisis Exploratorio:** visualizar correlaciones y patrones en los datos históricos
    - 📈 **Proyecciones:** ver los costos futuros proyectados con intervalos de confianza
    - 🤖 **Agente IA:** hacer preguntas en lenguaje natural sobre los resultados
    """)
    st.info("Selecciona una sección en el menú lateral para comenzar.")

# ─────────────────────────────────────────
# Página: Análisis Exploratorio
# ─────────────────────────────────────────
elif page == "Análisis Exploratorio":
    st.title("Análisis Exploratorio de Datos")
    st.warning("Pendiente: cargar datos y generar visualizaciones.")
    # TODO: cargar datos procesados y mostrar gráficos de correlación

# ─────────────────────────────────────────
# Página: Proyecciones
# ─────────────────────────────────────────
elif page == "Proyecciones":
    st.title("Proyecciones de Costos")
    st.warning("Pendiente: cargar modelos entrenados y mostrar proyecciones.")
    # TODO: cargar modelos y generar gráficos de forecasting con bandas de confianza

# ─────────────────────────────────────────
# Página: Agente IA
# ─────────────────────────────────────────
elif page == "Agente IA":
    st.title("Agente Conversacional")
    st.markdown("Pregunta al agente sobre los resultados del análisis y las proyecciones de costos.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Escribe tu pregunta aquí...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # TODO: conectar con agent.py una vez que el agente esté construido
        response = "El agente aún no está configurado. Completa los módulos src/agent.py primero."
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
