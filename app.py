import streamlit as st


# ================== CONFIGURACIÓN GENERAL ==================
st.set_page_config(
    page_title="UEV-ITM | DATA DAMZ SAS",
    layout="wide"
)

# ================== ESTILOS GLOBALES (SIDEBAR, TIPOGRAFÍA) ==================
st.markdown(
    """
    <style>
    /* Sidebar más limpio y corporativo */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #111827;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.0rem;
        padding-bottom: 1.5rem;
    }

    /* Texto del sidebar */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li, 
    section[data-testid="stSidebar"] span {
        font-size: 0.90rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== CONTENIDO DEL SIDEBAR ==================
with st.sidebar:
    st.markdown("#### 🧭 Navegación del tablero")
    st.markdown(
        """
        Este dashboard está organizado en cinco secciones:

        - **Descripción general**: visión ejecutiva y KPIs globales.  
        - **Matrículas y Desempeño**: riesgo por programa y asignatura.  
        - **Docentes y Cursos**: carga docente y resultados académicos.  
        - **Soporte y Atenciones**: motivos de soporte y tiempos de respuesta.  
        - **Conclusiones**: síntesis y recomendaciones estratégicas.

        Usa este menú para recorrer la historia completa del análisis.
        """
    )
    st.markdown("---")
    st.caption("Desarrollado por **DATA DAMZ SAS** · Analítica para educación virtual")

# ================== HEADER CORPORATIVO (MISMO ESTILO QUE EN LAS PÁGINAS) ==================
header_html = (
    '<div style="background: linear-gradient(90deg,#0f172a,#1e293b,#1e3a5f);'
    'padding: 26px 32px; border-radius: 0 0 22px 22px; border-bottom: 1px solid #111827;'
    'margin-bottom: 32px; display:flex; justify-content:space-between; align-items:center;'
    'box-shadow: 0 12px 28px rgba(0,0,0,0.35);">'
        '<div style="flex:1;">'
            '<div style="font-size:28px; font-weight:900; letter-spacing:0.08em; '
            'text-transform:uppercase; color:#bfdbfe;">'
                'DATA DAMZ SAS'
            '</div>'
            '<div style="font-size:18px; color:#e5e7eb; margin-top:6px; font-weight:300;">'
                'Transformamos datos en decisiones para la educación virtual.'
            '</div>'
        '</div>'
        '<div style="flex:1; text-align:right;">'
            '<div style="font-size:17px; color:#cbd5e1; font-weight:400;">'
                'Proyecto analítico · Unidad de Educación Virtual – ITM'
            '</div>'
            '<div style="font-size:16px; color:#94a3b8; margin-top:4px;">'
                'Periodo de análisis: <b>2024-1 y 2024-2</b>'
            '</div>'
        '</div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# ================== TÍTULO PRINCIPAL ==================
titulo_html = (
    '<h1 style="margin-bottom:0;">'
    'Unidad de Educación Virtual (UEV-ITM)'
    '</h1>'
    '<h3 style="margin-top:6px; color:#9ca3af; font-weight:400;">'
    'Análisis de deserción, rendimiento académico y soporte estudiantil en cursos virtuales'
    '</h3>'
)
st.markdown(titulo_html, unsafe_allow_html=True)

st.markdown(
    "Esta aplicación analítica es desarrollada por **DATA DAMZ SAS** en el marco del semillero de investigación "
    "de la UEV-ITM. Integra información de matrículas, docencia y soporte para apoyar la toma de decisiones "
    "sobre permanencia y calidad de la educación virtual."
)

# ================== PREGUNTA FOCAL DESTACADA ==================
st.markdown("<br>", unsafe_allow_html=True)

pregunta_html = (
    '<div style="border-radius:18px; border:1px solid #1f2937; padding:22px 26px; '
    'background:radial-gradient(circle at top left, #1d283a 0, #020617 65%); '
    'box-shadow:0 18px 35px rgba(15,23,42,0.65); margin-bottom:28px;">'
        '<div style="font-size:14px; color:#93c5fd; text-transform:uppercase; '
        'letter-spacing:0.16em;">'
            'Pregunta focal del proyecto'
        '</div>'
        '<div style="font-size:22px; font-weight:700; color:#e5e7eb; margin-top:10px; '
        'line-height:1.35;">'
            '¿Qué programas y asignaturas presentan mayor deserción, reprobación o cancelación '
            'y cuáles son los factores asociados a ese comportamiento?'
        '</div>'
        '<div style="font-size:15px; color:#cbd5f5; margin-top:12px; line-height:1.6; max-width:900px;">'
            'Con esta pregunta buscamos identificar <b>programas y cursos en situación de riesgo</b>, '
            'analizar cómo se relacionan los estados académicos con la carga docente y el soporte al estudiante, '
            'y generar insumos para decisiones de acompañamiento, rediseño de cursos y fortalecimiento de la '
            'experiencia en la educación virtual.'
        '</div>'
    '</div>'
)
st.markdown(pregunta_html, unsafe_allow_html=True)

# ================== DESCRIPCIÓN DE LAS PÁGINAS ==================
st.markdown(
    """
    ### Cómo está organizado el tablero

    Cada pestaña del menú lateral responde a un bloque de análisis específico:

    - **Descripción general**: resume los indicadores institucionales y explica cómo cada página se conecta con las preguntas P1–P5.  
    - **Matrículas y Desempeño**: profundiza en la deserción, reprobación y desempeño por programa, modalidad y asignatura.  
    - **Docentes y Cursos**: analiza la relación entre carga docente, tamaño de grupo y resultados académicos.  
    - **Soporte y Atenciones**: muestra los motivos más frecuentes de soporte, tiempos de respuesta y satisfacción.  
    - **Conclusiones**: integra los hallazgos y presenta recomendaciones estratégicas para la UEV-ITM.

    La idea es que quien navegue el tablero pueda seguir una **historia clara**: desde el contexto general,
    pasando por el detalle de programas, docentes y soporte, hasta llegar a una síntesis accionable.
    """
)

st.markdown(
    """
    <hr style="margin-top:40px; margin-bottom:10px; border: 1px solid #1e293b;">
    <p style="text-align:center; color:#64748b; font-size:13px;">
        Desarrollado por:<br>
        <b>Andrés Zapata Calle · Mateo Lozano Palacio · Zamir Bustamante Ruiz · Darwin Agudelo Deossa</b>
    </p>
    """,
    unsafe_allow_html=True
)
