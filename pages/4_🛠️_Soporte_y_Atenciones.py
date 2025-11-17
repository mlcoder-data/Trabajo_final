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
    sup = pd.read_csv("soporte_atenciones_focus.csv")
    return mat, sup

mat, sup = load_data()
mat["es_desercion"] = mat["estado_academico"] == "Cancelado"

# ================== HEADER + TÍTULO ==================
header_data_damz()

st.title("🎧 Soporte y Atenciones al Estudiante")

st.markdown(
    "En esta vista analizamos el comportamiento de la **mesa de ayuda y los canales de soporte** "
    "a los estudiantes virtuales. Desde DATA DAMZ SAS buscamos responder dos preguntas centrales:"
    "\n\n"
    "- ¿Qué tipos de problemas se presentan con mayor frecuencia (P3)?\n"
    "- ¿El tiempo de respuesta y la experiencia de soporte se relacionan con la deserción (P5)?"
)

# ================== FILTROS ==================
st.markdown("### Filtros de análisis")

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

mat_f = mat[
    mat["semestre"].isin(sem_sel)
    & mat["facultad"].isin(fac_sel)
    & mat["programa"].isin(prog_sel)
]

# ================== KPIs ==================
st.markdown("### Resumen de actividad de soporte y riesgo académico")

total_casos = len(sup_f)
prom_tiempo = sup_f["tiempo_respuesta_horas"].mean() if total_casos > 0 else 0
prom_satis = sup_f["satisfaccion_estudiante"].mean() if total_casos > 0 else 0

if not mat_f.empty:
    tasa_deserc_global = mat_f["es_desercion"].mean() * 100
else:
    tasa_deserc_global = 0

k1, k2, k3, k4 = st.columns(4)

card1 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Casos de soporte analizados</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{total_casos}</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Incluye todos los registros de soporte dentro de los filtros seleccionados.'
        '</div>'
    '</div>'
)

card2 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Tiempo respuesta promedio</div>'
        f'<div style="font-size:26px; font-weight:700; color:#e5e7eb; margin-top:4px;">{prom_tiempo:.1f} h</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Tiempo medio entre apertura y cierre del caso.'
        '</div>'
    '</div>'
)

card3 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Satisfacción del estudiante</div>'
        f'<div style="font-size:26px; font-weight:700; color:#4ade80; margin-top:4px;">{prom_satis:.2f} / 5</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Promedio de calificación posterior a la atención.'
        '</div>'
    '</div>'
)

card4 = (
    '<div style="background:#020617; border-radius:16px; padding:16px 18px; '
    'border:1px solid #1f2937;">'
        '<div style="font-size:13px; color:#9ca3af;">Tasa de deserción en matrículas</div>'
        f'<div style="font-size:26px; font-weight:700; color:#f97373; margin-top:4px;">{tasa_deserc_global:.1f}%</div>'
        '<div style="font-size:12px; color:#6b7280; margin-top:6px;">'
            'Calculada sobre las matrículas de los mismos segmentos (semestre, facultad, programa).'
        '</div>'
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
    "Este bloque permite abrir la conversación sobre la **carga operativa del soporte**, la velocidad de respuesta "
    "y el nivel de satisfacción percibido por los estudiantes, en contraste con la tasa de deserción observada en "
    "las matrículas del mismo contexto."
)

# =========================================================
# 1. MOTIVOS DE SOPORTE (P3) – GRÁFICO MEJORADO
# =========================================================
st.markdown("---")
st.markdown("### 1. Motivos de soporte más frecuentes (P3)")

if not sup_f.empty:
    motivo_agg = (
        sup_f.groupby("motivo")
        .size()
        .reset_index(name="casos")
        .sort_values("casos", ascending=False)
    )

    color_bar = "#60a5fa"

    chart_motivos = (
        alt.Chart(motivo_agg)
        .mark_bar(
            size=55,
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8,
        )
        .encode(
            x=alt.X("motivo:N", title="Motivo de soporte", sort="-y"),
            y=alt.Y("casos:Q", title="Número de casos"),
            color=alt.value(color_bar),
            tooltip=[
                alt.Tooltip("motivo:N", title="Motivo"),
                alt.Tooltip("casos:Q", title="Casos reportados"),
            ],
        )
        .properties(height=420)
    )

    labels_motivos = (
        alt.Chart(motivo_agg)
        .mark_text(
            align="center",
            baseline="bottom",
            dy=-4,
            color="#e5e7eb",
            fontSize=14,
            fontWeight="bold",
        )
        .encode(
            x=alt.X("motivo:N", sort="-y"),
            y=alt.Y("casos:Q"),
            text="casos:Q",
        )
    )

    st.altair_chart(chart_motivos + labels_motivos, use_container_width=True)

    st.markdown(
        """
        **Interpretación sugerida:**

        - Cada barra representa un **tipo de problema** que los estudiantes reportan al soporte.
        - La altura indica cuántos casos se han registrado para ese motivo.
        - Esta gráfica permite identificar rápidamente **en qué temas se concentra la demanda de soporte**:
          por ejemplo, si predominan las dificultades de acceso, problemas académicos, temas de plataforma, etc.

        Para la UEV-ITM, esta información es clave para priorizar:
        - Capacitación a estudiantes y docentes.
        - Mejoras en la plataforma virtual.
        - Recursos de autoayuda (tutoriales, guías, FAQs) enfocados en los problemas más frecuentes.
        """
    )
else:
    st.info("No hay registros de soporte con los filtros seleccionados.")

# =========================================================
# 2. TIEMPO DE RESPUESTA POR TIPO DE ATENCIÓN – MEJORADO
# =========================================================
st.markdown("---")
st.markdown("### 2. Tiempo de respuesta por tipo de atención")

if not sup_f.empty:
    tipo_agg = (
        sup_f.groupby("tipo_atencion", as_index=False)["tiempo_respuesta_horas"]
        .mean()
    )

    color_tipo = "#34d399"  # verde suave

    chart_tipo = (
        alt.Chart(tipo_agg)
        .mark_bar(
            size=55,
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8,
        )
        .encode(
            x=alt.X("tipo_atencion:N", title="Tipo de atención"),
            y=alt.Y("tiempo_respuesta_horas:Q", title="Tiempo respuesta promedio (horas)"),
            color=alt.value(color_tipo),
            tooltip=[
                alt.Tooltip("tipo_atencion:N", title="Tipo de atención"),
                alt.Tooltip("tiempo_respuesta_horas:Q", title="Horas promedio"),
            ],
        )
        .properties(height=380)
    )

    labels_tipo = (
        alt.Chart(tipo_agg)
        .mark_text(
            align="center",
            baseline="bottom",
            dy=-4,
            color="#e5e7eb",
            fontSize=13,
            fontWeight="bold",
        )
        .encode(
            x=alt.X("tipo_atencion:N"),
            y=alt.Y("tiempo_respuesta_horas:Q"),
            text=alt.Text("tiempo_respuesta_horas:Q", format=".1f"),
        )
    )

    st.altair_chart(chart_tipo + labels_tipo, use_container_width=True)

    st.markdown(
        """
        En este gráfico comparamos los **canales o tipos de atención** (por ejemplo: ticket, correo, llamada,
        chat, etc.):

        - El eje X muestra cada tipo de atención.
        - El eje Y indica el **tiempo promedio** que tarda en resolverse un caso en ese canal.

        Esto permite a la UEV-ITM identificar:
        - Qué canales son **más ágiles** y podrían priorizarse.
        - Qué canales presentan **mayores demoras** y requieren ajustes en procesos o en capacidad operativa.
        """
    )
else:
    st.info("No hay registros de soporte con los filtros seleccionados.")

# =========================================================
# 3. SATISFACCIÓN POR REGIÓN – GRÁFICO MEJORADO
# =========================================================
st.markdown("---")
st.markdown("### 3. Satisfacción del estudiante por región")

if not sup_f.empty:
    sat_reg = (
        sup_f.groupby("region", as_index=False)["satisfaccion_estudiante"]
        .mean()
    )

    base_sat = alt.Chart(sat_reg).encode(
        x=alt.X("region:N", title="Región"),
        y=alt.Y("satisfaccion_estudiante:Q", title="Satisfacción promedio (1 a 5)"),
    )

    puntos_sat = (
        base_sat
        .mark_circle(size=160, opacity=0.9)
        .encode(
            color=alt.value("#fbbf24"),
            tooltip=[
                alt.Tooltip("region:N", title="Región"),
                alt.Tooltip("satisfaccion_estudiante:Q", title="Satisfacción promedio"),
            ],
        )
    )

    linea_prom = (
        alt.Chart(sat_reg)
        .mark_rule(strokeDash=[6, 4], size=2, color="#6b7280")
        .encode(y="mean(satisfaccion_estudiante):Q")
    )

    st.altair_chart(puntos_sat + linea_prom, use_container_width=True)

    st.markdown(
        """
        Este gráfico muestra cómo valoran los estudiantes la **calidad del soporte** en cada región:

        - Cada punto es una región.
        - La posición en el eje Y indica la **satisfacción promedio** (en escala de 1 a 5).
        - La línea punteada representa el **promedio general**, lo que permite ver rápidamente
          qué regiones están por encima o por debajo de la media.

        Una lectura posible para la presentación:
        - Regiones con satisfacción por debajo del promedio pueden requerir **refuerzo de canales de soporte**,
          ajustes de horarios o acompañamiento adicional.
        - Regiones con niveles altos de satisfacción pueden servir como **referencia de buenas prácticas**.
        """
    )
else:
    st.info("No hay casos de soporte con los filtros seleccionados.")

# =========================================================
# 4. TIEMPO DE RESPUESTA VS DESERCIÓN (P5) – MEJORADO
# =========================================================
st.markdown("---")
st.markdown("### 4. Relación entre tiempo de respuesta y deserción (P5)")

if not sup_f.empty and not mat_f.empty:
    mat_seg = (
        mat_f.groupby(["semestre", "facultad", "programa"], as_index=False)
        .agg(
            matriculas=("id_estudiante", "count"),
            desertores=("es_desercion", "sum"),
        )
    )
    mat_seg["tasa_desercion_%"] = mat_seg["desertores"] / mat_seg["matriculas"] * 100

    sup_seg = (
        sup_f.groupby(["semestre", "facultad", "programa"], as_index=False)
        .agg(
            casos_soporte=("id_caso", "count"),
            tiempo_resp_prom=("tiempo_respuesta_horas", "mean"),
            satis_prom=("satisfaccion_estudiante", "mean"),
        )
    )

    seg = mat_seg.merge(
        sup_seg,
        on=["semestre", "facultad", "programa"],
        how="inner",
    )

    if not seg.empty:
        scatter_rel = (
            alt.Chart(seg)
            .mark_circle(opacity=0.85, stroke="#e5e7eb", strokeWidth=1.2)
            .encode(
                x=alt.X("tiempo_resp_prom:Q", title="Tiempo respuesta promedio (horas)"),
                y=alt.Y("tasa_desercion_%:Q", title="Tasa de deserción (%)"),
                size=alt.Size("casos_soporte:Q", title="N° casos de soporte", legend=None),
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
            .properties(height=420)
        )

        st.altair_chart(scatter_rel, use_container_width=True)

        st.markdown(
            """
            **Qué buscamos en este gráfico:**

            - Cada punto representa un segmento **semestre–facultad–programa**.
            - El eje X muestra el **tiempo de respuesta promedio** del soporte para ese segmento.
            - El eje Y indica la **tasa de deserción** de las matrículas.
            - El tamaño del punto refleja cuántos **casos de soporte** se atendieron, y el color la facultad.

            Si los puntos con tiempos de respuesta más altos tienden a ubicarse también en la parte superior
            (mayor deserción), podemos argumentar que **los tiempos de respuesta prolongados podrían estar
            asociados a mayor riesgo de abandono**.

            En caso de no observar una tendencia clara, el mensaje para las directivas puede ser que,
            según los datos actuales, la deserción parece estar más influenciada por otros factores
            (académicos, personales, de diseño de curso, etc.) y que el soporte, aunque importante,
            no es el único determinante.
            """
        )
    else:
        st.info("No se encontraron segmentos comunes entre soporte y matrículas para este análisis.")
else:
    st.info("Se requieren datos tanto de matrículas como de soporte para construir esta relación.")
