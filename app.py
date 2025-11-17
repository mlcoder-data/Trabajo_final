import streamlit as st

st.set_page_config(
    page_title="UEV-ITM | Deserción y Soporte",
    layout="wide"
)

st.markdown(
    """
    <h1 style="margin-bottom:0;">Unidad de Educación Virtual (UEV-ITM)</h1>
    <h3 style="margin-top:4px;color:#9ca3af;">Análisis de deserción, rendimiento y soporte en cursos virtuales 2024-1 y 2024-2</h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Esta aplicación forma parte del **semillero de investigación** y busca responder a la pregunta:

    >¿Qué programas y asignaturas presentan mayor deserción, reprobación o cancelación y cuáles son los factores asociados?

    Usa el menú de la izquierda para navegar por:

    - **Descripción general:** KPIs globales y respuestas resumidas a las preguntas de negocio.
    - **Matrículas y Desempeño:** detalle por programa, modalidad y asignatura.
    - **Docentes y Cursos:** carga docente y rendimiento.
    - **Soporte y Atenciones:** motivos, tiempos de respuesta y satisfacción.
    - **Conclusiones:** narrativa final para la presentación.
    """
)
