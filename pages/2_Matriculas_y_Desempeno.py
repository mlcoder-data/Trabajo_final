import streamlit as st
import pandas as pd
import altair as alt

st.title("🎓 Matrículas y Desempeño Académico")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    return mat, doc

mat, doc = load_data()

# Enlace con nombre de curso
mat_doc = mat.merge(doc[["id_curso", "nombre_curso", "id_docente"]], on="id_curso", how="left")

mat_doc["es_desercion"] = mat_doc["estado_academico"] == "Cancelado"
mat_doc["es_reprob"] = mat_doc["estado_academico"] == "Reprobado"
mat_doc["es_desercion_o_reprob"] = mat_doc["es_desercion"] | mat_doc["es_reprob"]

# ========= FILTROS =========
st.markdown("### Filtros")

c1, c2, c3 = st.columns(3)

semestres = sorted(mat_doc["semestre"].unique().tolist())
facultades = sorted(mat_doc["facultad"].unique().tolist())
modalidades = sorted(mat_doc["modalidad"].unique().tolist())

sem_sel = c1.multiselect("Semestre", semestres, default=semestres)
fac_sel = c2.multiselect("Facultad", facultades, default=facultades)
mod_sel = c3.multiselect("Modalidad", modalidades, default=modalidades)

df = mat_doc[
    mat_doc["semestre"].isin(sem_sel)
    & mat_doc["facultad"].isin(fac_sel)
    & mat_doc["modalidad"].isin(mod_sel)
]

# ========= KPIs LOCALES =========
st.markdown("### Resumen de matrículas filtradas")

k1, k2, k3, k4 = st.columns(4)

total_matr = len(df)
tasa_deserc = df["es_desercion"].mean() * 100 if total_matr > 0 else 0
tasa_reprob = df["es_reprob"].mean() * 100 if total_matr > 0 else 0
nota_prom = df["nota_final"].mean() if total_matr > 0 else 0

with k1:
    st.metric("Matrículas", total_matr)

with k2:
    st.metric("Deserción (Cancelado)", f"{tasa_deserc:.1f}%")

with k3:
    st.metric("Reprobación", f"{tasa_reprob:.1f}%")

with k4:
    st.metric("Nota promedio", f"{nota_prom:.2f}")

# ========= GRÁFICO 1: ESTADO POR PROGRAMA (RESPUESTA DIRECTA A P1) =========
st.markdown("---")
st.markdown("### 1. Estados académicos por programa")

if not df.empty:
    estados_prog = (
        df.groupby(["programa", "estado_academico"])
        .size()
        .reset_index(name="n")
    )

    chart_prog = (
        alt.Chart(estados_prog)
        .mark_bar()
        .encode(
            x=alt.X("programa:N", title="Programa", sort="-y"),
            y=alt.Y("n:Q", title="Número de matrículas"),
            color=alt.Color("estado_academico:N", title="Estado"),
            tooltip=["programa", "estado_academico", "n"],
        )
    )

    st.altair_chart(chart_prog, use_container_width=True)

    st.caption(
        "Este gráfico permite ver rápidamente **qué programas concentran más reprobados y cancelados**."
    )
else:
    st.info("No hay datos para los filtros seleccionados.")

# ========= TABLA: INDICADORES POR PROGRAMA =========
st.markdown("### 2. Indicadores de deserción y reprobación por programa")

if not df.empty:
    prog_ind = (
        df.groupby("programa")
        .agg(
            matrículas=("id_estudiante", "count"),
            deserciones=("es_desercion", "sum"),
            reprobaciones=("es_reprob", "sum"),
        )
    )
    prog_ind["tasa_desercion_%"] = prog_ind["deserciones"] / prog_ind["matrículas"] * 100
    prog_ind["tasa_reprob_%"] = prog_ind["reprobaciones"] / prog_ind["matrículas"] * 100
    prog_ind = prog_ind.sort_values("tasa_desercion_%", ascending=False)

    st.dataframe(prog_ind, use_container_width=True)

    st.caption(
        "Ordenado de mayor a menor tasa de deserción: aquí identificas los **programas críticos** para la pregunta focal."
    )

# ========= GRÁFICO 2: ASIGNATURAS (CURSOS) EN MAYOR RIESGO =========
st.markdown("---")
st.markdown("### 3. Asignaturas con mayor deserción/reprobación")

if not df.empty:
    curso_ind = (
        df.groupby("nombre_curso")
        .agg(
            matrículas=("id_estudiante", "count"),
            deserciones=("es_desercion", "sum"),
            reprobaciones=("es_reprob", "sum"),
        )
        .reset_index()
    )
    curso_ind["tasa_desercion_%"] = curso_ind["deserciones"] / curso_ind["matrículas"] * 100
    curso_ind["tasa_reprob_%"] = curso_ind["reprobaciones"] / curso_ind["matrículas"] * 100

    top_cursos = curso_ind.sort_values("tasa_desercion_%", ascending=False).head(10)

    chart_cursos = (
        alt.Chart(top_cursos)
        .mark_bar()
        .encode(
            x=alt.X("nombre_curso:N", title="Asignatura", sort="-y"),
            y=alt.Y("tasa_desercion_%:Q", title="Tasa de deserción (%)"),
            tooltip=[
                "nombre_curso",
                "matrículas",
                "deserciones",
                "reprobaciones",
                "tasa_desercion_%",
                "tasa_reprob_%",
            ],
        )
    )

    st.altair_chart(chart_cursos, use_container_width=True)

    st.caption(
        "Estas son las **asignaturas con mayor tasa de cancelación**. Puedes mencionar ejemplos específicos en la exposición."
    )

# ========= GRÁFICO 3: SEGMENTOS (MODALIDAD / SUBPERIODO) PARA P4 =========
st.markdown("---")
st.markdown("### 4. Segmentos de mayor riesgo (modalidad y subperiodo)")

if not df.empty:
    seg = (
        df.groupby(["modalidad", "subperiodo"])
        .agg(
            matrículas=("id_estudiante", "count"),
            deserciones=("es_desercion_o_reprob", "sum"),
        )
        .reset_index()
    )
    seg["tasa_desercion_reprob_%"] = seg["deserciones"] / seg["matrículas"] * 100

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
                "matrículas",
                "deserciones",
                "tasa_desercion_reprob_%",
            ],
        )
    )

    st.altair_chart(chart_seg, use_container_width=True)

    st.caption(
        "Aquí analizas **segmentos de estudiantes** por modalidad y subperiodo, para conectar con la P4."
    )
