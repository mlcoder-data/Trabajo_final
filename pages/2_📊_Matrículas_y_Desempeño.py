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

header_data_damz()

# ================== TÍTULO PRINCIPAL ==================
st.title("🎓 Matrículas y Desempeño Académico")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    return mat, doc

mat, doc = load_data()

# Unimos info de matrícula + curso/docente
df = mat.merge(
    doc[["id_curso", "nombre_curso", "id_docente", "facultad", "programa"]],
    on=["id_curso", "facultad", "programa"],
    how="left"
)

df["es_desercion"] = df["estado_academico"] == "Cancelado"
df["es_reprob"] = df["estado_academico"] == "Reprobado"
df["es_desercion_o_reprob"] = df["es_desercion"] | df["es_reprob"]

st.markdown(
    "En esta vista analizamos el comportamiento de las matrículas por **programa, modalidad y asignatura**, "
    "con énfasis en los estados académicos que están directamente relacionados con la deserción y el riesgo: "
    "**cancelado** y **reprobado**. Desde DATA DAMZ SAS buscamos que esta sección sea el punto de partida para "
    "identificar dónde se concentran los principales focos de alerta."
)

# ================== FILTROS ==================
st.markdown("### Filtros de análisis")

c1, c2, c3, c4 = st.columns(4)

semestres = sorted(df["semestre"].dropna().unique().tolist())
facultades = sorted(df["facultad"].dropna().unique().tolist())
programas = sorted(df["programa"].dropna().unique().tolist())
modalidades = sorted(df["modalidad"].dropna().unique().tolist())

sem_sel = c1.multiselect("Semestre", semestres, default=semestres)
fac_sel = c2.multiselect("Facultad", facultades, default=facultades)
prog_sel = c3.multiselect("Programa", programas, default=programas)
mod_sel = c4.multiselect("Modalidad", modalidades, default=modalidades)

df_f = df[
    df["semestre"].isin(sem_sel)
    & df["facultad"].isin(fac_sel)
    & df["programa"].isin(prog_sel)
    & df["modalidad"].isin(mod_sel)
]

# ================== KPIs LOCALES ==================
st.markdown("### Resumen de matrículas en los filtros seleccionados")

total_matr = len(df_f)
tasa_deserc = df_f["es_desercion"].mean() * 100 if total_matr > 0 else 0
tasa_reprob = df_f["es_reprob"].mean() * 100 if total_matr > 0 else 0
nota_prom = df_f["nota_final"].mean() if total_matr > 0 else 0

k1, k2, k3, k4 = st.columns(4)

card_m1 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Matrículas en el segmento</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{total_matr}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Total de registros que cumplen las condiciones de filtro actuales.'
        '</div>'
    '</div>'
)

card_m2 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Deserción (Cancelado)</div>'
        f'<div style="font-size:26px; font-weight:700; color:#f97373; margin-top:4px;">{tasa_deserc:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Proporción de matrículas con estado "Cancelado". Indica abandono formal del curso.'
        '</div>'
    '</div>'
)

card_m3 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Reprobación</div>'
        f'<div style="font-size:26px; font-weight:700; color:#facc15; margin-top:4px;">{tasa_reprob:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Porcentaje de matrículas que culminan en reprobación. Refleja dificultades académicas.'
        '</div>'
    '</div>'
)

card_m4 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Nota final promedio</div>'
        f'<div style="font-size:26px; font-weight:700; color:#4ade80; margin-top:4px;">{nota_prom:.2f}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Indicador de desempeño global del segmento analizado.'
        '</div>'
    '</div>'
)

with k1:
    st.markdown(card_m1, unsafe_allow_html=True)
with k2:
    st.markdown(card_m2, unsafe_allow_html=True)
with k3:
    st.markdown(card_m3, unsafe_allow_html=True)
with k4:
    st.markdown(card_m4, unsafe_allow_html=True)

st.markdown(
    "Estos cuatro indicadores permiten abrir la conversación con una lectura rápida del contexto: "
    "volumen de matrículas, nivel de deserción, nivel de reprobación y rendimiento promedio en el "
    "segmento seleccionado. Desde DATA DAMZ SAS sugerimos utilizar este bloque como introducción a la sección."
)

# ================== 1. ESTADOS POR PROGRAMA ==================
st.markdown("---")
st.markdown("### 1. Estados académicos por programa")

if not df_f.empty:
    estados_prog = (
        df_f.groupby(["programa", "estado_academico"])
        .size()
        .reset_index(name="n")
    )

    chart_prog = (
        alt.Chart(estados_prog)
        .mark_bar()
        .encode(
            x=alt.X("programa:N", title="Programa", sort="-y"),
            y=alt.Y("n:Q", title="Número de matrículas"),
            color=alt.Color("estado_academico:N", title="Estado académico"),
            tooltip=["programa", "estado_academico", "n"],
        )
    )

    st.altair_chart(chart_prog, use_container_width=True)

    st.markdown(
        """
        **Cómo leer este gráfico desde la perspectiva de gestión:**

        - Cada barra representa un programa académico dentro de los filtros seleccionados.
        - Los colores permiten comparar la proporción de **aprobados**, **reprobados** y **cancelados** en cada programa.
        - Un programa con barras altas en “Cancelado” o “Reprobado” indica un **riesgo académico** mayor.

        Como DATA DAMZ SAS, recomendamos que en la presentación se destaquen aquellos programas donde la franja
        de “Cancelado” y “Reprobado” es más visible, ya que allí se encuentran las principales oportunidades de
        intervención (acompañamiento, rediseño curricular, refuerzo docente, etc.).
        """
    )
else:
    st.info("No hay registros para los filtros seleccionados.")

# ================== 2. INDICADORES POR PROGRAMA ==================
st.markdown("### 2. Indicadores de deserción y reprobación por programa")

if not df_f.empty:
    prog_ind = (
        df_f.groupby("programa")
        .agg(
            matriculas=("id_estudiante", "count"),
            deserciones=("es_desercion", "sum"),
            reprobaciones=("es_reprob", "sum"),
        )
    )
    prog_ind["tasa_desercion_%"] = prog_ind["deserciones"] / prog_ind["matriculas"] * 100
    prog_ind["tasa_reprob_%"] = prog_ind["reprobaciones"] / prog_ind["matriculas"] * 100
    prog_ind = prog_ind.sort_values("tasa_desercion_%", ascending=False)

    st.dataframe(prog_ind, use_container_width=True)

    st.markdown(
        """
        Esta tabla complementa el gráfico anterior con una **lectura numérica precisa** por programa:

        - `matriculas`: volumen total de matrículas analizadas en el programa.
        - `deserciones`: cuántas de esas matrículas terminaron con estado “Cancelado”.
        - `reprobaciones`: cuántas terminaron en “Reprobado”.
        - `tasa_desercion_%` y `tasa_reprob_%`: indicadores porcentuales que facilitan la comparación entre programas,
          independientemente del tamaño de cada uno.

        En el diálogo con las directivas, esta tabla permite responder con precisión a preguntas como:
        *“¿qué tan grave es el problema en cada programa?”* y *“¿qué programas deberían priorizarse en un plan de acción?”*.
        """
    )
else:
    st.info("No hay registros para los filtros seleccionados.")

# ================== 3. ASIGNATURAS EN MAYOR RIESGO ==================
st.markdown("---")
st.markdown("### 3. Asignaturas con mayor tasa de deserción / reprobación")

if not df_f.empty:
    curso_ind = (
        df_f.groupby("nombre_curso")
        .agg(
            matriculas=("id_estudiante", "count"),
            deserciones=("es_desercion", "sum"),
            reprobaciones=("es_reprob", "sum"),
        )
        .reset_index()
    )
    curso_ind["tasa_desercion_%"] = curso_ind["deserciones"] / curso_ind["matriculas"] * 100
    curso_ind["tasa_reprob_%"] = curso_ind["reprobaciones"] / curso_ind["matriculas"] * 100

    top_cursos = curso_ind.sort_values("tasa_desercion_%", ascending=False).head(10)

    chart_cursos = (
        alt.Chart(top_cursos)
        .mark_bar()
        .encode(
            x=alt.X("nombre_curso:N", title="Asignatura", sort="-y"),
            y=alt.Y("tasa_desercion_%:Q", title="Tasa de deserción (%)"),
            tooltip=[
                "nombre_curso",
                "matriculas",
                "deserciones",
                "reprobaciones",
                "tasa_desercion_%",
                "tasa_reprob_%",
            ],
        )
    )

    st.altair_chart(chart_cursos, use_container_width=True)

    st.markdown(
        """
        En este gráfico nos enfocamos en el **nivel de asignatura**:

        - Se listan las 10 asignaturas con mayor tasa de deserción dentro de los filtros aplicados.
        - Cada barra muestra el porcentaje de matrículas canceladas sobre el total de matrículas de esa asignatura.
        - Adicionalmente, el tooltip permite ver cuántos estudiantes estuvieron inscritos, cuántos desertaron y cuántos reprobaron.

        Desde DATA DAMZ SAS sugerimos utilizar esta vista para identificar cursos "críticos" donde puede ser necesario:

        - Revisar la carga de trabajo y la estructura del curso.
        - Fortalecer el acompañamiento docente o las tutorías.
        - Coordinar acciones específicas entre la UEV y los programas responsables.
        """
    )
else:
    st.info("No hay registros para los filtros seleccionados.")

# ================== 4. SEGMENTOS (MODALIDAD Y SUBPERIODO) ==================
st.markdown("---")
st.markdown("### 4. Segmentos con mayor riesgo (modalidad y subperiodo)")

if not df_f.empty:
    seg = (
        df_f.groupby(["modalidad", "subperiodo"])
        .agg(
            matriculas=("id_estudiante", "count"),
            deserciones=("es_desercion_o_reprob", "sum"),
        )
        .reset_index()
    )
    seg["tasa_desercion_reprob_%"] = seg["deserciones"] / seg["matriculas"] * 100

    chart_seg = (
        alt.Chart(seg)
        .mark_bar()
        .encode(
            x=alt.X("modalidad:N", title="Modalidad"),
            y=alt.Y("tasa_desercion_reprob_%:Q", title="Tasa deserción+reprob (%)"),
            color="subperiodo:N",
            tooltip=[
                "modalidad",
                "subperiodo",
                "matriculas",
                "deserciones",
                "tasa_desercion_reprob_%",
            ],
        )
    )

    st.altair_chart(chart_seg, use_container_width=True)

    st.markdown(
        """
        Este análisis por **modalidad (AMV/APV)** y **subperiodo** permite entender si el riesgo está asociado a:

        - La forma en que se oferta la asignatura (por ejemplo, si alguna modalidad concentra más cancelaciones).
        - Momentos específicos del calendario académico (subperiodos con mayor presión o acumulación de actividades).

        Este tipo de segmentación complementa el análisis por programa y asignatura y ayuda a la UEV-ITM a decidir
        si las acciones deben ser únicamente académicas o también **operativas y de calendario**.
        """
    )
else:
    st.info("No hay registros para los filtros seleccionados.")

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
