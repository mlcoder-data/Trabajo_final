import streamlit as st
import pandas as pd
import altair as alt

st.title("👩‍🏫 Docentes y Cursos Virtuales")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    return mat, doc

mat, doc = load_data()

# ===================== PREPARACIÓN =====================
# Unimos matrícula + info del curso y docente
df = mat.merge(
    doc,
    on=["id_curso", "semestre", "facultad", "programa"],
    how="left"
)

df["es_reprobado"] = df["estado_academico"] == "Reprobado"
df["es_cancelado"] = df["estado_academico"] == "Cancelado"

# Filtros
st.markdown("### Filtros")

c1, c2 = st.columns(2)

semestres = sorted(df["semestre"].dropna().unique().tolist())
facultades = sorted(df["facultad"].dropna().unique().tolist())

sem_sel = c1.multiselect("Semestre", semestres, default=semestres)
fac_sel = c2.multiselect("Facultad", facultades, default=facultades)

df_f = df[df["semestre"].isin(sem_sel) & df["facultad"].isin(fac_sel)]

# Agregamos por curso–docente (tamaño de grupo y rendimiento)
curso_doc = (
    df_f.groupby(
        ["id_curso", "nombre_curso", "id_docente",
         "facultad", "programa", "antiguedad_docente_semestres"],
        as_index=False
    )
    .agg(
        estudiantes=("id_estudiante", "nunique"),
        nota_promedio=("nota_final", "mean"),
        tasa_reprobacion=("es_reprobado", "mean"),
        tasa_desercion=("es_cancelado", "mean"),
    )
)

if not curso_doc.empty:
    curso_doc["tasa_reprobacion"] *= 100
    curso_doc["tasa_desercion"] *= 100

# ===================== KPIs (P2) =====================
st.markdown("### 🧮 Resumen de carga y rendimiento")

k1, k2, k3, k4 = st.columns(4)

if not curso_doc.empty:
    prom_tam_grupo = curso_doc["estudiantes"].mean()
    prom_nota = curso_doc["nota_promedio"].mean()
    prom_reprob = curso_doc["tasa_reprobacion"].mean()
    prom_deser = curso_doc["tasa_desercion"].mean()
else:
    prom_tam_grupo = prom_nota = prom_reprob = prom_deser = 0

with k1:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Cursos analizados</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{len(curso_doc)}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Cursos virtuales con matrícula en los filtros</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Tamaño promedio de grupo</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{prom_tam_grupo:.1f}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Estudiantes por curso</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Nota promedio</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{prom_nota:.2f}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Promedio general de los cursos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Reprobación y deserción</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{prom_reprob:.1f}% / {prom_deser:.1f}%</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Promedios por curso</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    👉 Estos indicadores te permiten introducir la **P2**:  
    _“¿Existen patrones entre el rendimiento académico y la carga docente (tamaño de grupo, número de estudiantes por docente)?”_
    """
)

# ===================== 1. Tamaño de grupo vs nota promedio =====================
st.markdown("---")
st.markdown("### 1. Tamaño de grupo vs rendimiento por curso (P2)")

if not curso_doc.empty:
    chart_carga = (
        alt.Chart(curso_doc)
        .mark_circle(size=80)
        .encode(
            x=alt.X("estudiantes:Q", title="Tamaño de grupo (n° estudiantes)"),
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

    st.caption(
        "Cada punto es un curso. Con este gráfico puedes comentar si los **grupos más grandes** tienden a tener "
        "notas promedio más bajas o si no se observa un patrón claro."
    )
else:
    st.info("No hay datos para los filtros seleccionados.")

# ===================== 2. Antigüedad docente vs nota promedio =====================
st.markdown("### 2. Antigüedad docente y resultados académicos")

if not df_f.empty:
    # Agregamos por docente
    doc_agg = (
        df_f.groupby(
            ["id_docente", "facultad", "programa", "antiguedad_docente_semestres"],
            as_index=False
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

    chart_ant = (
        alt.Chart(doc_agg)
        .mark_circle(size=80)
        .encode(
            x=alt.X("antiguedad_docente_semestres:Q", title="Antigüedad (semestres)"),
            y=alt.Y("nota_promedio:Q", title="Nota promedio del docente"),
            color=alt.Color("facultad:N", title="Facultad"),
            size=alt.Size("cursos:Q", title="N° cursos dictados"),
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

    st.caption(
        "Aquí puedes analizar si los **docentes con más antigüedad** concentran mejores resultados "
        "o si la brecha no es tan fuerte."
    )

    st.markdown("### 3. Docentes con mayores tasas de reprobación/deserción")

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
                "programa",
                "cursos",
                "estudiantes",
                "nota_promedio",
                "tasa_reprobacion",
                "tasa_desercion",
            ]
        ],
        use_container_width=True,
    )

    st.caption(
        "Esta tabla no es para ‘señalar’ docentes en público, pero sí para mostrar a las directivas que el "
        "dashboard permite identificar **focos específicos de acompañamiento**."
    )
else:
    st.info("No hay datos para los filtros seleccionados.")
