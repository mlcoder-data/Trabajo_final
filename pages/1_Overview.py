import streamlit as st
import pandas as pd

st.title("📌 Descripción general y preguntas de negocio")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    sup = pd.read_csv("soporte_atenciones_focus.csv")
    return mat, doc, sup

mat, doc, sup = load_data()

# ========= CÁLCULOS BASE =========
mat["es_desercion_o_reprob"] = mat["estado_academico"].isin(["Cancelado", "Reprobado"])
mat["es_desercion"] = mat["estado_academico"] == "Cancelado"
mat["es_reprob"] = mat["estado_academico"] == "Reprobado"

total_estudiantes = mat["id_estudiante"].nunique()
total_matriculas = len(mat)
total_programas = mat["programa"].nunique()
total_cursos = doc["id_curso"].nunique()
total_docentes = doc["id_docente"].nunique()
total_casos_soporte = sup["id_caso"].nunique()

tasa_desercion_global = mat["es_desercion"].mean() * 100
tasa_reprob_global = mat["es_reprob"].mean() * 100
nota_prom_global = mat["nota_final"].mean()

# Programas con mayor deserción+reprobación
prog_agg = (
    mat.groupby("programa")
    .agg(
        estudiantes=("id_estudiante", "nunique"),
        desertores=("es_desercion_o_reprob", "sum"),
        cancelados=("es_desercion", "sum"),
        reprobados=("es_reprob", "sum")
    )
)
prog_agg["tasa_desercion_reprob"] = prog_agg["desertores"] / prog_agg["estudiantes"] * 100
top_prog_riesgo = (
    prog_agg.sort_values("tasa_desercion_reprob", ascending=False)
    .head(3)
    .reset_index()
)

# ========= LAYOUT DE KPIs (COLUMNAS CON COLOR) =========
st.markdown("### 🧮 Panorama general de la operación virtual 2024-1 / 2024-2")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Estudiantes únicos</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{total_estudiantes}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">En todos los programas virtuales</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Matrículas registradas</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{total_matriculas}</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Incluye repeticiones de estudiante por curso</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Tasa global de deserción</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{tasa_desercion_global:.1f}%</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Matrículas con estado "Cancelado"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:16px;border-radius:12px;border:1px solid #1f2937;">
        <div style="color:#9ca3af;font-size:13px;">Tasa global de reprobación</div>
        <div style="font-size:26px;font-weight:700;margin-top:4px;">{tasa_reprob_global:.1f}%</div>
        <div style="color:#6b7280;font-size:12px;margin-top:6px;">Matrículas con estado "Reprobado"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    > La nota final promedio de todos los cursos es de **{nota_prom_global:.2f}**  
    > y se registran **{total_cursos} cursos virtuales**, atendidos por **{total_docentes} docentes**  
    > y respaldados por **{total_casos_soporte} casos de soporte registrados**.
    """
)

# ========= BLOQUE P1: Programas en mayor riesgo =========
st.markdown("---")
st.markdown("### P1. ¿Qué programas presentan mayor deserción, reprobación o cancelación?")

st.markdown(
    """
    Para esta pregunta se calculó, por programa:

    - Número de estudiantes únicos.
    - Cuántos de ellos tuvieron al menos una matrícula **cancelada o reprobada**.
    - La **tasa de deserción+reprobación** = desertores / estudiantes.
    """
)

st.markdown("**Top 3 programas con mayor tasa de deserción + reprobación:**")

st.dataframe(
    top_prog_riesgo.rename(
        columns={
            "programa": "Programa",
            "estudiantes": "Estudiantes únicos",
            "desertores": "Estudiantes con cancelación/reprobación",
            "cancelados": "Cancelados",
            "reprobados": "Reprobados",
            "tasa_desercion_reprob": "Tasa deserción+reprob (%)",
        }
    ),
    use_container_width=True
)

st.markdown(
    """
    👉 En la exposición puedes comentar que estos programas requieren **seguimiento prioritario**,  
    y luego profundizar en la página de **Matrículas y Desempeño** para ver qué asignaturas 
    específicas explican estas tasas.
    """
)

# ========= BLOQUE P2–P5: RESUMEN NARRATIVO =========
st.markdown("---")
st.markdown("### 🎯 Relación con las demás preguntas de negocio")

col_p_izq, col_p_der = st.columns(2)

with col_p_izq:
    st.markdown("#### P2. Rendimiento vs carga docente")
    st.markdown(
        """
        - En la página **Docentes y Cursos** se calcula, por curso y docente:
          - Tamaño de grupo (n° estudiantes por curso).
          - Promedio de nota por curso/docente.
        - Con esto se observa si grupos más grandes tienden a tener **menores notas promedio**
          o más reprobación.
        """
    )

    st.markdown("#### P3. Problemas de soporte y riesgo de deserción")
    st.markdown(
        """
        - La página **Soporte y Atenciones** muestra:
          - Frecuencia de cada **motivo** de atención.
          - Distribución por **tipo de atención**.
        - Además, se integran los datos de matrículas y soporte por **semestre–facultad–programa**
          para ver si los programas con más casos de soporte también presentan **mayor tasa de deserción**.
        """
    )

with col_p_der:
    st.markdown("#### P4. Segmentos con mayor propensión al abandono")
    st.markdown(
        """
        - Con la información disponible, los segmentos más claros son:
          - **Programa** y **facultad**.
          - **Modalidad** (AMV / APV).
          - **Subperiodo** (A, B, C).
        - En **Matrículas y Desempeño** podrás filtrar por estos campos y comparar
          tasas de deserción y reprobación entre segmentos.
        """
    )

    st.markdown("#### P5. Impacto del tiempo de respuesta del soporte")
    st.markdown(
        """
        - Se agrupan los datos por **semestre–facultad–programa**, calculando:
          - Tasa de deserción.
          - Tiempo de respuesta promedio.
          - Satisfacción promedio.
        - En **Soporte y Atenciones** se muestra un gráfico de dispersión para ver
          si los programas con **tiempos de respuesta más altos** tienden a mostrar
          **mayor deserción** (o si no hay una relación fuerte).
        """
    )

st.markdown("---")
st.markdown(
    """
    Con esta página de **Descripción general** tienes:

    - Los **KPIs clave** para abrir la presentación.
    - Un **top de programas en mayor riesgo**, directamente conectado con la pregunta focal.
    - Un mapa claro de **qué página del dashboard responde cada pregunta P1–P5**.
    """
)
