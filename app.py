import streamlit as st

# ---------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------
st.set_page_config(
    page_title="UEV-ITM | DATA DAMZ SAS",
    layout="wide"
)

# ---------------------------------------------------
# BARRA SUPERIOR: MARCA DE LA EMPRESA
# ---------------------------------------------------
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#0f172a,#1e293b,#1e3a5f);
        padding: 28px 34px;
        border-radius: 0 0 22px 22px;
        border-bottom: 1px solid #111827;
        margin-bottom: 32px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow: 0 12px 28px rgba(0,0,0,0.35);
    ">
        
        <!-- IZQUIERDA -->
        <div style="flex:1;">
            <div style="
                font-size:26px;
                font-weight:900;
                letter-spacing:0.08em;
                text-transform:uppercase;
                color:#bfdbfe;">
                DATA DAMZ SAS
            </div>
            
            <div style="
                font-size:17px;
                color:#e5e7eb;
                margin-top:6px;
                font-weight:300;">
                Transformamos datos en decisiones para la educación virtual.
            </div>
        </div>

        <!-- DERECHA -->
        <div style="flex:1; text-align:right;">
            <div style="
                font-size:16px;
                color:#cbd5e1;
                font-weight:400;">
                Proyecto analítico · Unidad de Educación Virtual – ITM
            </div>
            <div style="
                font-size:15px;
                color:#94a3b8;
                margin-top:4px;">
                Periodo de análisis: <b>2024-1 y 2024-2</b>
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# TITULO PRINCIPAL UEV
# ---------------------------------------------------
st.markdown(
    """
    <h1 style="margin-bottom:0;">
        Unidad de Educación Virtual (UEV-ITM)
    </h1>
    <h3 style="margin-top:6px; color:#9ca3af; font-weight:400;">
        Análisis de deserción, rendimiento y soporte en cursos virtuales 2024-1 y 2024-2
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Esta aplicación analítica es desarrollada por DATA DAMZ SAS en el marco del semillero de investigación
    de la UEV. El tablero integra información de matrículas, docencia y soporte al estudiante para apoyar la toma 
    de decisiones sobre permanencia y calidad de la educación virtual.
    """
)

# ---------------------------------------------------
# PREGUNTA FOCAL DESTACADA
# ---------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        border-radius:18px;
        border:1px solid #1f2937;
        padding:18px 22px;
        background:radial-gradient(circle at top left, #1d283a 0, #020617 55%);
        box-shadow:0 18px 35px rgba(15,23,42,0.65);
        margin-bottom:22px;
    ">
        <div style="font-size:13px; color:#93c5fd; text-transform:uppercase; letter-spacing:0.16em;">
            Pregunta focal del proyecto
        </div>
        <div style="font-size:20px; font-weight:700; color:#e5e7eb; margin-top:6px;">
            ¿Qué programas y asignaturas presentan mayor deserción, reprobación o cancelación
            y cuáles son los factores asociados a ese comportamiento?
        </div>
        <div style="font-size:13px; color:#cbd5f5; margin-top:10px; line-height:1.55;">
            Con esta pregunta buscamos identificar <b>programas y cursos en situación de riesgo</b>, entender 
            cómo se relacionan los estados académicos con la carga docente y con el soporte al estudiante, 
            y proponer insumos para decisiones estratégicas de acompañamiento, rediseño de cursos y 
            fortalecimiento de los servicios de apoyo académico y tecnológico.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SECCIÓN: CÓMO NAVEGAR EL TABLERO
# ---------------------------------------------------
st.markdown(
    """
    ### Navegación del tablero

    Utilice el menú de la izquierda para explorar las distintas vistas del análisis:

    - **Descripción general:** indicadores globales y resumen de las preguntas de negocio.
    - **Matrículas y Desempeño:** análisis detallado por programa, modalidad y asignatura.
    - **Docentes y Cursos:** relación entre carga docente, tamaño de grupo y rendimiento.
    - **Soporte y Atenciones:** motivos de soporte, tiempos de respuesta y satisfacción estudiantil.
    - **Conclusiones:** principales hallazgos y líneas de acción sugeridas para la UEV.

    Cada página está diseñada para aportar una pieza del diagnóstico, de manera que, en conjunto,
    el tablero permita responder de forma sólida a la pregunta focal planteada por la UEV y DATA DAMZ SAS.
    """
)
