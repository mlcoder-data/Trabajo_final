import streamlit as st
import pandas as pd
import altair as alt

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


# ================== CARGA DE DATOS ==================
@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    return mat, doc

mat, doc = load_data()

# Unimos matrículas con información del curso y del docente
# -> mantenemos los nombres de las columnas de matrícula SIN sufijos
# -> las columnas que se repitan en docentes tendrán el sufijo "_doc"
df = mat.merge(doc, on="id_curso", how="left", suffixes=("", "_doc"))

df["es_reprobado"] = df["estado_academico"] == "Reprobado"
df["es_cancelado"] = df["estado_academico"] == "Cancelado"

# ================== HEADER + TÍTULO ==================
header_data_damz()

st.title("👩‍🏫 Docentes y Cursos Virtuales")

st.markdown(
    "En esta sección analizamos la relación entre **carga docente** y **resultados académicos**. "
    "Como DATA DAMZ SAS, nuestro objetivo es ofrecer a la UEV-ITM evidencia para responder a la pregunta: "
    "_¿cómo influyen el tamaño de grupo, la experiencia docente y la oferta de cursos en el rendimiento y la deserción?_"
)

# ================== FILTROS ==================
st.markdown("### Filtros de análisis")

c1, c2, c3 = st.columns(3)

semestres = sorted(df["semestre"].dropna().unique().tolist())
facultades = sorted(df["facultad"].dropna().unique().tolist())
programas = sorted(df["programa"].dropna().unique().tolist())

sem_sel = c1.multiselect("Semestre", semestres, default=semestres)
fac_sel = c2.multiselect("Facultad", facultades, default=facultades)
prog_sel = c3.multiselect("Programa", programas, default=programas)

df_f = df[
    df["semestre"].isin(sem_sel)
    & df["facultad"].isin(fac_sel)
    & df["programa"].isin(prog_sel)
]

# ================== AGREGACIONES ==================
# Por curso-docente: tamaño de grupo, nota promedio, tasas
if not df_f.empty:
    curso_doc = (
        df_f.groupby(
            [
                "id_curso",
                "nombre_curso",
                "id_docente",
                "facultad",
                "programa",
                "antiguedad_docente_semestres",  # viene del CSV de docentes
            ],
            as_index=False,
        )
        .agg(
            estudiantes=("id_estudiante", "nunique"),
            nota_promedio=("nota_final", "mean"),
            tasa_reprobacion=("es_reprobado", "mean"),
            tasa_desercion=("es_cancelado", "mean"),
        )
    )
    curso_doc["tasa_reprobacion"] *= 100
    curso_doc["tasa_desercion"] *= 100
else:
    curso_doc = pd.DataFrame()

# Por docente: consolidado de cursos, estudiantes y resultados
if not df_f.empty:
    doc_agg = (
        df_f.groupby(
            ["id_docente", "facultad", "antiguedad_docente_semestres"],
            as_index=False,
        )
        .agg(
            cursos=("id_curso", "nunique"),
            estudiantes=("id_estudiante", "nunique"),
            nota_promedio=("nota_final", "mean"),
            tasa_reprobacion=("es_reprobado", "mean"),
            tasa_desercion=("es_cancelado", "mean"),
        )
    )
    doc_agg["tasa_reprobacion"] *= 100
    doc_agg["tasa_desercion"] *= 100
else:
    doc_agg = pd.DataFrame()

# ================== KPIs ==================
st.markdown("### Resumen de carga y desempeño")

if not curso_doc.empty:
    prom_tam_grupo = curso_doc["estudiantes"].mean()
    prom_nota = curso_doc["nota_promedio"].mean()
    prom_reprob = curso_doc["tasa_reprobacion"].mean()
    prom_deser = curso_doc["tasa_desercion"].mean()
    n_cursos = len(curso_doc)
    n_docentes = curso_doc["id_docente"].nunique()
else:
    prom_tam_grupo = prom_nota = prom_reprob = prom_deser = 0
    n_cursos = n_docentes = 0

k1, k2, k3, k4 = st.columns(4)

card1 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Cursos virtuales analizados</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{n_cursos}</div>'
        f'<div style="font-size:12px; color:#6b7280; margin-top:6px;">Dictados por {n_docentes} docentes.</div>'
    '</div>'
)

card2 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Tamaño promedio de grupo</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{prom_tam_grupo:.1f}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">Estudiantes por curso.</div>'
    '</div>'
)

card3 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Nota promedio de los cursos</div>'
        f'<div style="font-size:26px; font-weight:700; color:#4ade80; margin-top:4px;">{prom_nota:.2f}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">Promedio de nota final por curso.</div>'
    '</div>'
)

card4 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Reprobación y deserción promedio</div>'
        f'<div style="font-size:26px; font-weight:700; color:#f97373; margin-top:4px;">{prom_reprob:.1f}% / {prom_deser:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">Promedio por curso (reprobado / cancelado).</div>'
    '</div>'
)

with k1:
    st.markdown(card1, unsafe_allow_html=True)
with k2:
    st.markdown(card2, unsafe_allow_html=True)
with k3:
    st.markdown(card3, unsafe_allow_html=True)
with k4:
    st.markdown(card4, unsafe_allow_html=True)

st.markdown(
    "Estos indicadores resumen la **escala de la operación docente** y el nivel general de rendimiento. "
    "Son útiles para abrir la conversación sobre carga, tamaño de grupo y resultados académicos."
)

# ================== 1. TAMAÑO DE GRUPO VS NOTA (POR CURSO) ==================
st.markdown("---")
st.markdown("### 1. Tamaño de grupo vs. nota promedio por curso")

if not curso_doc.empty:
    chart_carga = (
        alt.Chart(curso_doc)
        .mark_circle(size=80)
        .encode(
            x=alt.X("estudiantes:Q", title="Tamaño de grupo (número de estudiantes)"),
            y=alt.Y("nota_promedio:Q", title="Nota promedio del curso"),
            color=alt.Color("facultad:N", title="Facultad"),
            tooltip=[
                "nombre_curso",
                "programa",
                "facultad",
                "id_docente",
                "estudiantes",
                "nota_promedio",
                "tasa_reprobacion",
                "tasa_desercion",
            ],
        )
    )

    st.altair_chart(chart_carga, use_container_width=True)

    st.markdown(
        """
        **Cómo interpretar este gráfico:**

        - Cada punto representa un **curso específico** (un docente dictando una asignatura).
        - El eje X muestra el **tamaño de grupo** (número de estudiantes matriculados).
        - El eje Y muestra la **nota promedio final** de ese curso.
        - El color indica la **facultad**, lo que permite observar si hay patrones por unidad académica.

        Este gráfico responde a la pregunta de si los cursos con grupos más numerosos tienden a obtener
        resultados académicos más bajos. En la presentación se puede resaltar si se observa una tendencia
        clara descendente o si el comportamiento es más disperso, indicando que el tamaño de grupo no es el
        único factor determinante.
        """
    )
else:
    st.info("No hay datos suficientes para construir este gráfico con los filtros seleccionados.")

# ================== 2. ANTIGÜEDAD DOCENTE Y RESULTADOS ==================
st.markdown("---")
st.markdown("### 2. Antigüedad del docente y desempeño académico")

if not doc_agg.empty:
    chart_ant = (
        alt.Chart(doc_agg)
        .mark_circle(size=90)
        .encode(
            x=alt.X(
                "antiguedad_docente_semestres:Q",
                title="Antigüedad como docente virtual (semestres)"
            ),
            y=alt.Y("nota_promedio:Q", title="Nota promedio del docente"),
            size=alt.Size("cursos:Q", title="Número de cursos dictados"),
            color=alt.Color("facultad:N", title="Facultad"),
            tooltip=[
                "id_docente",
                "facultad",
                "cursos",
                "estudiantes",
                "nota_promedio",
                "tasa_reprobacion",
                "tasa_desercion",
            ],
        )
    )

    st.altair_chart(chart_ant, use_container_width=True)

    st.markdown(
        """
        **Lectura sugerida para este gráfico:**

        - Cada punto es un **docente**.
        - En el eje X se observa la **antigüedad** del docente en semestres.
        - En el eje Y, la **nota promedio** de todos sus cursos.
        - El tamaño del círculo indica cuántos **cursos ha dictado** (mayor tamaño = más carga).
        - El color diferencia las facultades.

        Esta visualización ayuda a explorar si la **experiencia docente** está asociada con mejores resultados
        (por ejemplo, si los docentes con más semestres tienden a concentrarse en la parte superior del gráfico),
        o si los resultados son similares independientemente de la antigüedad.

        En la conversación con las directivas, permite discutir temas como:
        - Necesidad de programas de **formación docente** para quienes están iniciando.
        - Reconocimiento de docentes con desempeño sostenido en el tiempo.
        """
    )
else:
    st.info("No hay datos suficientes para analizar la antigüedad docente con los filtros seleccionados.")

# ================== 3. DOCENTES CON MAYOR REPROBACIÓN / DESERCIÓN ==================
st.markdown("---")
st.markdown("### 3. Docentes con mayores tasas de reprobación y deserción")

if not doc_agg.empty:
    top_doc = (
        doc_agg.sort_values("tasa_reprobacion", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    st.dataframe(
        top_doc[
            [
                "id_docente",
                "facultad",
                "cursos",
                "estudiantes",
                "nota_promedio",
                "tasa_reprobacion",
                "tasa_desercion",
            ]
        ],
        use_container_width=True,
    )

    st.markdown(
        """
        Esta tabla no busca señalar personas, sino identificar **patrones de riesgo** asociados a la práctica docente:

        - Se listan los 10 docentes con mayor **tasa de reprobación** promedio en sus cursos.
        - También se incluye la **tasa de deserción**, el número de cursos dictados y el número de estudiantes atendidos.
        - Es un insumo para que la UEV-ITM pueda **ofrecer acompañamiento pedagógico** o revisar condiciones
          particulares de los cursos a cargo de estos docentes (complejidad de contenidos, tipo de estudiantes,
          modalidad, etc.).

        Como DATA DAMZ SAS, recomendamos tratar esta tabla como una herramienta interna de gestión académica,
        y no como un elemento de exposición pública con nombres propios.
        """
    )
else:
    st.info("No hay información suficiente para construir esta tabla con los filtros actuales.")

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
