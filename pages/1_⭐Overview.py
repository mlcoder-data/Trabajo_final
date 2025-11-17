import streamlit as st
import pandas as pd


# ================== HEADER CORPORATIVO ==================
def header_data_damz():
    header_html = (
        '<div style="background: linear-gradient(90deg,#0f172a,#1e293b,#1e3a5f);'
        'padding: 26px 32px; border-radius: 0 0 22px 22px; border-bottom: 1px solid #111827;'
        'margin-bottom: 38px; display:flex; justify-content:space-between; align-items:center;'
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

header_data_damz()

# ================== TÍTULO PRINCIPAL ==================

st.title("📌 Descripción general")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    sup = pd.read_csv("soporte_atenciones_focus.csv")
    return mat, doc, sup

mat, doc, sup = load_data()

# ================== CÁLCULOS PRINCIPALES ==================
mat["es_desercion"] = mat["estado_academico"] == "Cancelado"
mat["es_reprob"] = mat["estado_academico"] == "Reprobado"
mat["es_desercion_o_reprob"] = mat["es_desercion"] | mat["es_reprob"]

total_estudiantes = mat["id_estudiante"].nunique()
total_matriculas = len(mat)
total_programas = mat["programa"].nunique()
total_cursos = doc["id_curso"].nunique()
total_docentes = doc["id_docente"].nunique()
total_casos_soporte = sup["id_caso"].nunique()

tasa_desercion_global = mat["es_desercion"].mean() * 100
tasa_reprob_global = mat["es_reprob"].mean() * 100
nota_prom_global = mat["nota_final"].mean()

# Top 3 programas en riesgo (deserción + reprobación)
prog_agg = (
    mat.groupby("programa")
    .agg(
        estudiantes=("id_estudiante", "nunique"),
        desertores=("es_desercion_o_reprob", "sum"),
        cancelados=("es_desercion", "sum"),
        reprobados=("es_reprob", "sum"),
    )
)
prog_agg["tasa_desercion_reprob"] = (
    prog_agg["desertores"] / prog_agg["estudiantes"] * 100
)
top_prog_riesgo = (
    prog_agg.sort_values("tasa_desercion_reprob", ascending=False)
    .head(3)
    .reset_index()
)

# ================== SUBTÍTULO ==================
st.markdown(
    "Esta vista resume el estado general de la operación virtual y conecta el tablero "
    "con las preguntas de negocio definidas por la UEV y DATA DAMZ SAS."
)

st.markdown("")

# ================== KPIs EN CARDS (MISMO ESTILO QUE app.py) ==================
col1, col2, col3, col4 = st.columns(4)

card_1 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Estudiantes únicos</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{total_estudiantes}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'En todos los programas con matrícula virtual'
        '</div>'
    '</div>'
)

card_2 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Matrículas registradas</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{total_matriculas}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Incluye estudiantes que cursan más de una asignatura'
        '</div>'
    '</div>'
)

card_3 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Tasa global de deserción</div>'
        f'<div style="font-size:26px; font-weight:700; color:#f97373; margin-top:4px;">{tasa_desercion_global:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Porcentaje de matrículas con estado "Cancelado"'
        '</div>'
    '</div>'
)

card_4 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Tasa global de reprobación</div>'
        f'<div style="font-size:26px; font-weight:700; color:#facc15; margin-top:4px;">{tasa_reprob_global:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Porcentaje de matrículas con estado "Reprobado"'
        '</div>'
    '</div>'
)

with col1:
    st.markdown(card_1, unsafe_allow_html=True)
with col2:
    st.markdown(card_2, unsafe_allow_html=True)
with col3:
    st.markdown(card_3, unsafe_allow_html=True)
with col4:
    st.markdown(card_4, unsafe_allow_html=True)

st.markdown(
    f"> La nota final promedio de todos los cursos es de **{nota_prom_global:.2f}**. "
    f"El sistema cuenta con **{total_cursos} cursos virtuales**, atendidos por "
    f"**{total_docentes} docentes** y respaldados por **{total_casos_soporte} casos de soporte registrados**."
)

# ================== TOP PROGRAMAS EN RIESGO (PREGUNTA FOCAL) ==================
st.markdown("---")
st.markdown("### Programas con mayor riesgo de deserción y reprobación")

st.markdown(
    "A continuación se muestran los programas con mayor **tasa combinada de deserción y reprobación**. "
    "Esta tabla sirve como punto de partida para la pregunta focal del proyecto."
)

if not top_prog_riesgo.empty:
    tabla_prog = top_prog_riesgo.rename(
        columns={
            "programa": "Programa",
            "estudiantes": "Estudiantes únicos",
            "desertores": "Con cancelación o reprobación",
            "cancelados": "Cancelados",
            "reprobados": "Reprobados",
            "tasa_desercion_reprob": "Tasa deserción+reprob (%)",
        }
    )
    st.dataframe(tabla_prog, use_container_width=True)
else:
    st.info("No se encontraron programas con registros suficientes para este cálculo.")

st.markdown(
    "Desde la perspectiva de DATA DAMZ SAS y la UEV-ITM, estos programas deben ser considerados "
    "**prioritarios para el diseño de estrategias de acompañamiento**, revisión de contenidos y "
    "ajustes en la oferta virtual."
)

# ================== RELACIÓN CON LAS PREGUNTAS DE NEGOCIO ==================
st.markdown("---")
st.markdown("### Cómo se conectan las demás páginas con las preguntas de negocio")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### P2. Rendimiento vs. carga docente")
    st.markdown(
        "- En la página **Docentes y Cursos** analizamos el tamaño de grupo, la carga docente y la nota "
        "promedio por curso.\n"
        "- Esto permite identificar si los cursos con mayor número de estudiantes presentan mayores niveles "
        "de reprobación o resultados más bajos."
    )

    st.markdown("#### P3. Problemas de soporte y riesgo de deserción")
    st.markdown(
        "- En **Soporte y Atenciones** se clasifican los casos según su motivo y tipo de atención.\n"
        "- Al cruzar esta información con las tasas de deserción, podemos ver si los programas con más "
        "incidencias de soporte tienden a registrar también mayor abandono."
    )

with col_right:
    st.markdown("#### P4. Segmentos con mayor propensión al abandono")
    st.markdown(
        "- A partir de los filtros por **programa, facultad, modalidad y subperiodo**, la página de "
        "**Matrículas y Desempeño** permite ubicar los segmentos con mayores tasas de cancelación y reprobación.\n"
        "- Esto aporta una base objetiva para focalizar intervenciones."
    )

    st.markdown("#### P5. Impacto del tiempo de respuesta del soporte")
    st.markdown(
        "- La vista de **Soporte y Atenciones** incorpora el tiempo de respuesta y la satisfacción del estudiante.\n"
        "- Al relacionar estos indicadores con la deserción por programa y semestre, podemos evaluar si los "
        "tiempos de respuesta están influyendo en la permanencia."
    )

st.markdown("---")
st.markdown(
    "En síntesis, esta página de **Descripción general** entrega una visión ejecutiva de la operación virtual y "
    "explica cómo cada sección del tablero aporta evidencia para responder la pregunta focal definida por la UEV "
    "y DATA DAMZ SAS."
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
