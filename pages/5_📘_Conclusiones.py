import streamlit as st

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


# ================== HEADER + TÍTULO ==================
header_data_damz()

st.title("📘 Conclusiones y Recomendaciones Estratégicas")

st.markdown(
    """
    Esta sección presenta una síntesis ejecutiva del análisis realizado por **DATA DAMZ SAS** con base en 
    las matrículas, el rendimiento académico, la carga docente y la actividad de soporte en los periodos 
    **2024-1 y 2024-2** de la Unidad de Educación Virtual del ITM.

    El objetivo es ofrecer una lectura clara y fundamentada que permita a la institución tomar **decisiones 
    estratégicas basadas en evidencia**, respondiendo directamente a la **Pregunta Focal** del estudio.
    """
)

# ================== PREGUNTA FOCAL ==================
st.markdown("---")
st.markdown("### 🎯 Pregunta Focal del Proyecto")

st.markdown(
    """
    <div style="
        background:#0f172a; 
        padding:22px 26px; 
        border-radius:14px; 
        border:1px solid #1e293b;
        font-size:19px; 
        color:#e2e8f0;">
        <b>¿Qué programas y asignaturas presentan mayor deserción, reprobación o cancelación 
        y cuáles son los factores asociados a ese comportamiento?</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ================== CONCLUSIONES PRINCIPALES ==================
st.markdown("---")
st.subheader("📌 Conclusiones Principales")

st.markdown(
    """
    A partir de la integración y análisis de las tres fuentes de información (matrículas, docentes y soporte), 
    se destacan las siguientes conclusiones clave:
    """
)

st.markdown(
    """
    #### 1️⃣ Programas con mayor nivel de riesgo académico
    - Se identifican programas con **tasas elevadas de cancelación y reprobación**, lo que evidencia una 
      necesidad urgente de acompañamiento académico.
    - Estos programas comparten características como **altos tamaños de grupo**, cursos con baja nota promedio 
      y estudiantes con mayores dificultades para sostener la continuidad.

    #### 2️⃣ El tamaño de grupo influye en el rendimiento
    - En los cursos con grupos más numerosos, se observa una **tendencia a un menor promedio de notas**.
    - Este patrón sugiere que la carga docente y la dinámica de grupos grandes pueden estar afectando 
      la calidad del acompañamiento académico.

    #### 3️⃣ Diferencias significativas en el desempeño docente
    - Algunos docentes presentan **tasas más altas de reprobación**, lo cual no necesariamente implica 
      mal desempeño, sino que puede relacionarse con:
        - complejidad de contenidos,
        - perfiles de estudiantes,
        - saturación de carga académica.
    - Este grupo debe recibir **acompañamiento pedagógico focalizado**.

    #### 4️⃣ El soporte atiende principalmente problemas de tipo académico y acceso
    - Los motivos más frecuentes están relacionados con:
        - dificultades académicas,
        - problemas personales,
        - accesos a plataforma.
    - Esto indica que el soporte está absorbiendo parte del impacto de la **experiencia estudiantil virtual**.

    #### 5️⃣ Los tiempos de respuesta NO muestran una relación directa con la deserción
    - No se observa una correlación evidente entre los **tiempos de respuesta del soporte** y la 
      **tasa de deserción**.
    - Esto sugiere que la deserción está mucho más vinculada a **factores académicos** que a factores técnicos.

    #### 6️⃣ Las regiones con menor satisfacción requieren intervención
    - Algunas regiones presentan niveles de satisfacción por debajo del promedio, indicando posibles 
      brechas de infraestructura o de acompañamiento institucional.
    """
)


# ================== RECOMENDACIONES ==================
st.markdown("---")
st.subheader("🧭 Recomendaciones Estratégicas para la UEV – ITM")

st.markdown(
    """
    Basados en los hallazgos obtenidos, DATA DAMZ SAS propone las siguientes líneas de acción estratégicas:

    ### 🟦 1. Fortalecer los programas con alto riesgo académico
    - Implementar tutorías de refuerzo y acompañamiento personalizado.
    - Revisar mallas curriculares y metodologías de evaluación.
    - Reducir el número de estudiantes por curso cuando sea posible.

    ### 🟦 2. Capacitar y acompañar a docentes con mayor carga o complejidad en sus cursos
    - Ofrecer talleres de metodologías activas y estrategias para grupos grandes.
    - Monitorear sistemáticamente métricas de rendimiento docente.

    ### 🟦 3. Optimizar la gestión de soporte estudiantil
    - Crear rutas rápidas de solución para los motivos más frecuentes.
    - Fortalecer guías de autoayuda y contenido educativo preventivo.
    - Implementar un sistema de priorización inteligente según el tipo de caso.

    ### 🟦 4. Mejorar la experiencia virtual en regiones con menor satisfacción
    - Incrementar disponibilidad de personal en horarios de alta demanda.
    - Evaluar infraestructura tecnológica por región.

    ### 🟦 5. Profundizar en el seguimiento longitudinal del estudiante
    - Integrar analítica predictiva para identificar estudiantes en riesgo antes de que cancelen.
    - Conectar datos de matrícula, interacción en plataforma y soporte para una visión 360° del estudiante.
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
