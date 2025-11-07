import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load data ---
data = pd.read_csv(r"./data_limpia_inmobiliaria.csv")
# data = pd.read_csv(r"C:\Users\jcama\Desktop\Dashboard\data_limpia_inmobiliaria.csv")
data["Fecha Creación"] = pd.to_datetime(data["Fecha Creación"])

# --- Page config ---
st.set_page_config(page_title="Leads Dashboard", layout="wide")

# --- Sidebar filters ---
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Fecha inicio", data["Fecha Creación"].min().date())
end_date = st.sidebar.date_input("Fecha fin", data["Fecha Creación"].max().date())
provincia = st.sidebar.multiselect(
    "Provincia", options=data["Provincia"].unique(), default=data["Provincia"].unique()
)
estado_civil = st.sidebar.multiselect(
    "Estado Civil",
    options=data["Estado Civil"].unique(),
    default=data["Estado Civil"].unique(),
)
medio_captacion = st.sidebar.multiselect(
    "Medio de Captación",
    options=data["Medio De Captacion"].unique(),
    default=data["Medio De Captacion"].unique(),
)
canal_entrada = st.sidebar.multiselect(
    "Canal de Entrada",
    options=data["Canal De Entrada"].unique(),
    default=data["Canal De Entrada"].unique(),
)

# --- Filter data ---
filtered_df = data[
    (data["Fecha Creación"].dt.date >= start_date)
    & (data["Fecha Creación"].dt.date <= end_date)
    & (data["Provincia"].isin(provincia))
    & (data["Estado Civil"].isin(estado_civil))
    & (data["Medio De Captacion"].isin(medio_captacion))
    & (data["Canal De Entrada"].isin(canal_entrada))
]


# --- Tabs ---
tab_selection = st.sidebar.selectbox(
    "Selecciona la pestaña",
    ["Proyecto Relacionado", "Áreas más y menos valoradas", "Nivel de Interés"],
)


# --- Function to render 4 charts in 2x2 grid ---
def render_4charts(figures):
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    chart_rows = [row1_col1, row1_col2, row2_col1, row2_col2]

    for i, fig in enumerate(figures):
        chart_rows[i].plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )


# --- TAB: Proyecto Relacionado ---
if tab_selection == "Proyecto Relacionado":
    st.header("Proyecto Relacionado")

    fig1 = px.bar(
        filtered_df,
        x="Proyectos Relacionados",
        color="Canal De Entrada",
        title="Proyectos vs Canal de Entrada",
        barmode="group",
    )

    heatmap_data = filtered_df.pivot_table(
        index="Proyectos Relacionados",
        columns="Nivel De Interes",
        aggfunc="size",
        fill_value=0,
    )
    fig2 = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="YlGnBu",
        labels=dict(x="Nivel de Interés", y="Proyecto", color="Cantidad"),
    )

    age_avg = filtered_df.groupby("Proyectos Relacionados")["Edad"].mean().reset_index()
    fig3 = px.scatter(
        age_avg,
        x="Proyectos Relacionados",
        y="Edad",
        size="Edad",
        color="Edad",
        title="Edad promedio por proyecto",
    )

    fig4 = px.box(
        filtered_df,
        x="Proyectos Relacionados",
        y="Número Interacciones",
        color="Proyectos Relacionados",
        title="Número de interacciones por proyecto",
    )

    render_4charts([fig1, fig2, fig3, fig4])


# --- TAB: Áreas más y menos valoradas ---
elif tab_selection == "Áreas más y menos valoradas":
    st.header("Áreas más y menos valoradas")

    fig1 = px.violin(
        filtered_df,
        x="Área Social más valorada",
        y="Número Interacciones",
        color="Nivel De Interes",
        box=True,
        points="all",
        title="Área más valorada vs Interacciones",
    )

    fig2 = px.scatter(
        filtered_df,
        x="Área Social menos valorada",
        y="Número Interacciones",
        color="Nivel De Interes",
        title="Interacciones vs Área menos valorada",
    )

    heatmap_data = filtered_df.pivot_table(
        index="Área Social más valorada",
        columns="Provincia",
        aggfunc="size",
        fill_value=0,
    )
    fig3 = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        labels=dict(x="Provincia", y="Área más valorada", color="Cantidad"),
    )

    fig4 = px.box(
        filtered_df,
        x="Área Social menos valorada",
        y="Edad",
        color="Área Social menos valorada",
        title="Edad vs Área menos valorada",
    )

    render_4charts([fig1, fig2, fig3, fig4])


# --- TAB: Nivel de Interés ---
elif tab_selection == "Nivel de Interés":
    st.header("Nivel de Interés")

    fig1 = px.bar(
        filtered_df,
        x="Nivel De Interes",
        color="Canal De Entrada",
        barmode="group",
        title="Nivel de Interés vs Canal de Entrada",
    )

    fig2 = px.scatter(
        filtered_df,
        x="Nivel De Interes",
        y="Número Interacciones",
        color="Proyectos Relacionados",
        title="Interacciones por Nivel de Interés",
    )

    fig3 = px.box(
        filtered_df,
        x="Nivel De Interes",
        y="Edad",
        color="Nivel De Interes",
        title="Edad vs Nivel de Interés",
    )

    heatmap_data = filtered_df.pivot_table(
        index="Nivel De Interes",
        columns="Proyectos Relacionados",
        aggfunc="size",
        fill_value=0,
    )
    fig4 = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(x="Proyecto", y="Nivel de Interés", color="Cantidad"),
    )

    render_4charts([fig1, fig2, fig3, fig4])
