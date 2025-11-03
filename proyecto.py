# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Dashboard Inmobiliario")

# @st.cache_data
# def load_data():
#     data = pd.read_excel("./transformed_leads.xlsx")
#     return data

# df = load_data()

# st.sidebar.header("Controles")
# chart_type = st.sidebar.selectbox(
#     "Selecciona el tipo de gráfico",
#     ["Line Chart", "Bar Chart", "Pie Chart"]
# )

# if chart_type == "Line Chart":
#     fig = px.line(df, x="Fecha", y="Ventas", title="Ventas por Fecha")
#     st.plotly_chart(fig, use_container_width=True)

# elif chart_type == "Bar Chart":
#     fig = px.bar(df, x="Agente", y="Ventas", title="Ventas por Agente")
#     st.plotly_chart(fig, use_container_width=True)

# elif chart_type == "Pie Chart":
#     fig = px.pie(df, names="Ciudad", values="Ventas", title="Ventas por Ciudad")
#     st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Mascotas vs Nivel de interés")

# Cargar los datos desde Excel
df = pd.read_excel("./data.xlsx")
# df = pd.read_excel("./transformed_leads.xlsx")


# Controles de seleccion
st.sidebar.header("Controles")
chart_type = st.sidebar.selectbox(
    "Selecciona el tipo de gráfico",
    ["Line Chart", "Bar Chart", "Pie Chart"]
)






# Filtrar niveles de interés
niveles_seleccionados = ['compró', 'alto', 'medio', 'bajo']
df_filtrado = df[df['Nivel De Interes'].isin(niveles_seleccionados)]

#  Crear tabla de conteo
tabla_mascotas = (
    df_filtrado.groupby(["Tiene mascotas (si,no)", "Nivel De Interes"])
    .size()
    .reset_index(name="Número de Leads")
)

# Crear gráfico interactivo con Plotly
if chart_type == "Bar Chart":
    fig = px.bar(
        tabla_mascotas,
        x="Tiene mascotas (si,no)",
        # y="N°",
        y="Número de Leads",
        color="Nivel De Interes",
        barmode="stack",
        title="Mascotas vs Nivel de interés",
        labels={
            "Tiene mascotas (si,no)": "¿Tiene mascotas?",
            "Número de Leads": "Cantidad de Leads"
        }
    )

#  Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)

# elif chart_type == "Pie Chart":
#      fig = px.pie(df, names="Ciudad", values="Ventas", title="Ventas por Ciudad")
#      st.plotly_chart(fig, use_container_width=True)

