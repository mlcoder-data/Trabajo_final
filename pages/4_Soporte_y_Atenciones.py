import streamlit as st
import pandas as pd
import altair as alt

st.title("🎧 Soporte y Atenciones al Estudiante")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    sup = pd.read_csv("soporte_atenciones_focus.csv")
    return mat, sup

mat, sup = load_data()

# ===================== FILTROS =====================
st.markdown("### Filtros")

c1, c2, c3, c4 = st.columns(4)

semestres = sorted(sup["semestre"].dropna().unique().tolist())
facultades = sorted(sup["facultad"].dropna().unique().tolist())
programas = sorted(sup["programa"].dropna().unique().tolist())
regiones = sorted(sup["region"].dropna().unique().tolist())

sem_sel = c1.multiselect("Semestre", semestres, default=semestres)
fac_sel = c2.multiselect("Facultad", facultades, default=facultades)
prog_sel = c3.multiselect("Programa", programas, default=programas)
reg_sel = c4.multiselect("Región", regiones, default=regiones)

sup_f = sup[
    sup["semestre"].isin(sem_sel)
    & sup["facultad"].isin(fac_sel)
    & sup["programa"].isin(prog_sel)
    & sup["region"].isin(reg_sel)
]

# Para P5: agregamos también matrículas por combinaciones semestre–facultad–programa
mat_f = mat[
    mat["semestre"].isin(sem_sel)
    & mat["facultad"].isin(fac_sel)
    & mat["programa"].isin(prog_sel)
]

# ===================== KPIs =====================
st.markdown("### 🧮 Resumen de soporte y riesgo académico")

k1, k2, k3, k4 = st.columns(4)

total_casos = len(sup_f)
prom_tiempo = sup_f["tiempo_respuesta_horas"].mean() if not sup_f.empty else 0
prom_satis = sup_f["satisfaccion_estudiante"].mean() if not sup_f.empty else 0

# Tasa global de deserción de las matrículas en estos filtros
if not mat_f.empty:
    tasa_deserc_global = (mat_f["estado_academico"] == "Cancelado").mean() * 100
else:
    tasa_deserc_global = 0

with k1:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Casos de soporte</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{total_casos}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Registros en mesa de ayuda</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Tiempo respuesta promedio</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{prom_tiempo:.1f} h</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Entre apertura y cierre del caso</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Satisfacción promedio</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{prom_satis:.2f}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Escala de 1 a 5</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Tasa de deserción</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{tasa_deserc_global:.1f}%</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Sobre matrículas en estos filtros</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    Aquí introduces **P3** y **P5**:  
    - ¿Qué problemas de soporte son más frecuentes?  
    - ¿Cómo se relacionan el tiempo de respuesta y la satisfacción con la deserción?
    """
)

# ===================== 1. Motivos y tipo de atención (P3) =====================
st.markdown("---")
st.markdown("### 1. ¿Qué problemas de soporte son más frecuentes? (P3)")

if not sup_f.empty:
    # Casos por motivo
    motivo_agg = sup_f.groupby("motivo").size().reset_index(name="casos")

    chart_motivo = (
        alt.Chart(motivo_agg)
        .mark_bar()
        .encode(
            x=alt.X("motivo:N", title="Motivo", sort="-y"),
            y=alt.Y("casos:Q", title="Número de casos"),
            tooltip=["motivo", "casos"],
        )
    )
    st.altair_chart(chart_motivo, use_container_width=True)

    st.caption(
        "Permite hablar de los **tipos de problema más frecuentes** (académico, tecnológico, plataforma, etc.)."
    )

    # Tiempo de respuesta por tipo de atención
    tipo_agg = (
        sup_f.groupby("tipo_atencion", as_index=False)["tiempo_respuesta_horas"]
        .mean()
    )

    st.markdown("### 2. Tiempo de respuesta por tipo de atención")

    chart_tipo = (
        alt.Chart(tipo_agg)
        .mark_bar()
        .encode(
            x=alt.X("tipo_atencion:N", title="Tipo de atención"),
            y=alt.Y("tiempo_respuesta_horas:Q", title="Tiempo respuesta promedio (h)"),
            tooltip=["tipo_atencion", "tiempo_respuesta_horas"],
        )
    )

    st.altair_chart(chart_tipo, use_container_width=True)

    st.caption(
        "Te ayuda a identificar si algún tipo de canal (correo, mesa de ayuda, etc.) es **especialmente lento**."
    )
else:
    st.info("No hay casos de soporte con los filtros seleccionados.")

# ===================== 3. Satisfacción por región =====================
st.markdown("---")
st.markdown("### 3. Satisfacción del estudiante por región")

if not sup_f.empty:
    sat_reg = (
        sup_f.groupby("region", as_index=False)["satisfaccion_estudiante"]
        .mean()
    )

    chart_sat = (
        alt.Chart(sat_reg)
        .mark_circle(size=120)
        .encode(
            x=alt.X("region:N", title="Región"),
            y=alt.Y("satisfaccion_estudiante:Q", title="Satisfacción promedio (1–5)"),
            tooltip=["region", "satisfaccion_estudiante"],
        )
    )

    st.altair_chart(chart_sat, use_container_width=True)

    st.caption(
        "Muestra si hay **diferencias regionales en la experiencia de soporte**."
    )
else:
    st.info("No hay casos de soporte con los filtros seleccionados.")

# ===================== 4. Relación tiempo de respuesta – deserción (P5) =====================
st.markdown("---")
st.markdown("### 4. ¿Influye el tiempo de respuesta en la deserción? (P5)")

if not mat_f.empty and not sup_f.empty:
    # Agregamos matrículas por semestre–facultad–programa
    mat_seg = (
        mat_f.groupby(["semestre", "facultad", "programa"], as_index=False)
        .agg(
            matriculas=("id_estudiante", "count"),
            desertores=("estado_academico", lambda x: (x == "Cancelado").sum()),
        )
    )
    mat_seg["tasa_desercion_%"] = mat_seg["desertores"] / mat_seg["matriculas"] * 100

    # Agregamos soporte en el mismo nivel
    sup_seg = (
        sup_f.groupby(["semestre", "facultad", "programa"], as_index=False)
        .agg(
            casos_soporte=("id_caso", "count"),
            tiempo_resp_prom=("tiempo_respuesta_horas", "mean"),
            satis_prom=("satisfaccion_estudiante", "mean"),
        )
    )

    # Unimos
    seg = mat_seg.merge(
        sup_seg,
        on=["semestre", "facultad", "programa"],
        how="inner",
    )

    if not seg.empty:
        chart_rel = (
            alt.Chart(seg)
            .mark_circle(size=100)
            .encode(
                x=alt.X("tiempo_resp_prom:Q", title="Tiempo respuesta promedio (h)"),
                y=alt.Y("tasa_desercion_%:Q", title="Tasa de deserción (%)"),
                size=alt.Size("casos_soporte:Q", title="N° casos de soporte"),
                color=alt.Color("facultad:N", title="Facultad"),
                tooltip=[
                    "semestre",
                    "facultad",
                    "programa",
                    "casos_soporte",
                    "tiempo_resp_prom",
                    "satis_prom",
                    "tasa_desercion_%",
                ],
            )
        )

        st.altair_chart(chart_rel, use_container_width=True)

        st.caption(
            "Cada punto es un **segmento semestre–facultad–programa**. "
            "Si los puntos con mayor tiempo de respuesta tienden a estar arriba, "
            "puedes argumentar que **tiempos de respuesta altos se asocian con mayor deserción**."
        )
    else:
        st.info("No hay suficientes combinaciones comunes entre matrícula y soporte para este análisis.")
else:
    st.info("Se necesitan datos tanto de matrículas como de soporte para este análisis.")
