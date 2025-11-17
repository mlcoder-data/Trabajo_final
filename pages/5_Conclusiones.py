import streamlit as st
import pandas as pd

st.title("🧩 Conclusiones")

@st.cache_data
def load_data():
    mat = pd.read_csv("matriculaslimpias.csv")
    doc = pd.read_csv("docenteslimpios.csv")
    sup = pd.read_csv("soporte_atenciones_focus.csv")
    return mat, doc, sup

mat, doc, sup = load_data()

# --------- Cálculos rápidos para poner ejemplos concretos ----------
mat["es_desercion"] = mat["estado_academico"] == "Cancelado"
mat["es_reprob"] = mat["estado_academico"] == "Reprobado"

prog_agg = (
    mat.groupby("programa")
    .agg(
        matrículas=("id_estudiante", "count"),
        deserciones=("es_desercion", "sum"),
        reprobaciones=("es_reprob", "sum"),
    )
)
prog_agg["tasa_desercion_%"] = prog_agg["deserciones"] / prog_agg["matrículas"] * 100
prog_agg["tasa_reprob_%"] = prog_agg["reprobaciones"] / prog_agg["matrículas"] * 100
top_prog = prog_agg.sort_values("tasa_desercion_%", ascending=False).head(3)

motivo_agg = sup.groupby("motivo").size().reset_index(name="casos")
motivo_agg = motivo_agg.sort_values("casos", ascending=False).head(3)

tiempo_prom = sup["tiempo_respuesta_horas"].mean()
satis_prom = sup["satisfaccion_estudiante"].mean()

# --------- Texto estructurado ---------
st.markdown("## 🎯 Resumen por pregunta de negocio")

# P1
st.markdown("### P1. ¿Qué programas y asignaturas presentan mayor deserción, reprobación o cancelación?")

if not top_prog.empty:
    lista_prog = ", ".join(top_prog.index.tolist())
else:
    lista_prog = "algunos programas específicos con tasas superiores al promedio"

st.markdown(
    f"""
- Los datos muestran que programas como **{lista_prog}** presentan las **tasas más altas de deserción**.
- En la página de **Matrículas y Desempeño** se identifican también las **asignaturas con mayor concentración de cancelaciones y reprobaciones**, lo que permite priorizar acciones de acompañamiento y revisión curricular.
"""
)

# P2
st.markdown("### P2. ¿Existen patrones entre el rendimiento académico y la carga docente?")

st.markdown(
    """
- En **Docentes y Cursos** se observa la relación entre **tamaño de grupo** y **nota promedio por curso**.
- El gráfico de dispersión permite ver si los cursos con grupos muy grandes tienden a presentar:
  - Menores notas promedio.
  - Mayores tasas de reprobación o deserción.
- Además, el análisis por **antigüedad docente** muestra si los docentes con más experiencia concentran mejores resultados o si las diferencias no son tan grandes.
"""
)

# P3
if not motivo_agg.empty:
    motivos_texto = ", ".join(motivo_agg["motivo"].tolist())
else:
    motivos_texto = "los principales motivos registrados en la mesa de ayuda"

st.markdown("### P3. ¿Qué tipos de problemas de soporte son más frecuentes?")

st.markdown(
    f"""
- A partir de la tabla **soporte_atenciones_focus**, se identifica que los motivos más frecuentes son:  
  **{motivos_texto}**.
- Esta información permite orientar campañas de **prevención, capacitación o mejoras en la plataforma**, 
  enfocadas en los problemas que realmente viven los estudiantes.
"""
)

# P4
st.markdown("### P4. ¿Qué segmentos de estudiantes muestran mayor propensión al abandono?")

st.markdown(
    """
- En la pestaña **Matrículas y Desempeño** se comparan tasas de deserción y reprobación por:
  - **Programa** y **facultad**.
  - **Modalidad** (AMV / APV).
  - **Subperiodo** (A, B, C).
- Con esto se pueden identificar **segmentos críticos** (por ejemplo, ciertos programas en modalidad APV y subperiodos específicos) donde vale la pena:
  - Reforzar el acompañamiento académico.
  - Revisar la carga de contenidos y la evaluación.
"""
)

# P5
st.markdown("### P5. ¿Cuál es el impacto del tiempo de respuesta del soporte en la permanencia?")

st.markdown(
    f"""
- El tiempo de respuesta promedio del soporte es de aproximadamente **{tiempo_prom:.1f} horas**, con una satisfacción media de **{satis_prom:.2f} / 5**.
- En la pestaña **Soporte y Atenciones** se combina la información de:
  - **Tiempo de respuesta promedio**.
  - **Número de casos de soporte**.
  - **Tasa de deserción por semestre–facultad–programa**.
- El gráfico de dispersión permite discutir si los segmentos con **tiempos de respuesta más altos** tienden a mostrar **mayor deserción**, o si la relación no es tan directa.
"""
)

st.markdown("---")
st.markdown(
    """
## 🧵 Mensaje de cierre para las directivas

- El dashboard integra de forma coherente **matrículas, docencia y soporte**, lo que permite pasar de mirar solo cifras sueltas a entender la **experiencia completa del estudiante virtual**.
- A partir de los hallazgos, la UEV puede:
  - Priorizar **programas y asignaturas** con mayor riesgo de deserción.
  - Revisar la **distribución de grupos y carga docente**.
  - Fortalecer los **canales de soporte** que presenten mayores tiempos de respuesta.
- El objetivo final es que este tablero no sea solo un informe de cierre, sino una **herramienta viva de monitoreo y toma de decisiones** para mejorar la permanencia y el éxito académico en la educación virtual.
"""
)
