import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sqlalchemy import create_engine



# Your PostgreSQL connection string
connection_string = "postgresql://postgres:fUkQJyRhLsHaigOKtuVzDAaKOxNoMSzc@trolley.proxy.rlwy.net:58949/railway"


# Create SQLAlchemy engine
engine = create_engine(connection_string)

# Example: load an entire table into a DataFrame
table_name = "data_limpia_inmobiliaria"  # 🔹 Replace with the actual table name
data = pd.read_sql_table(table_name, engine)


# --- Load data ---
# data = pd.read_csv(r"./data_limpia_inmobiliaria.csv")
# data = pd.read_csv(r"C:\Users\jcama\Desktop\Dashboard\data_limpia_inmobiliaria.csv")
# data["Fecha Creación"] = pd.to_datetime(data["Fecha Creación"])
data["Fecha Creación"] = pd.to_datetime(data["Fecha Creación"], format="mixed", errors="coerce")
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
    st.header("Dashboard Proyecto Inmobiliaria")
    
    niveles_seleccionados = ['compró', 'alto', 'medio', 'bajo']
    df_filtrado = filtered_df[filtered_df['Nivel De Interes'].isin(niveles_seleccionados)]

    tabla_mascotas = (
        df_filtrado.groupby(["Tiene mascotas (si,no)", "Nivel De Interes"])
        .size()
        .reset_index(name="Número de Leads")
    )
    
    # ?? grafico 1
    # ?? =====================================================================
    fig1 = px.bar(
        tabla_mascotas,
        x="Tiene mascotas (si,no)",
        y="Número de Leads",
        color="Nivel De Interes",
        barmode="stack",
        title="Mascotas vs Nivel de Interés",
        labels={
            "Tiene mascotas (si,no)": "¿Tiene mascotas?",
            "Número de Leads": "Cantidad de Leads"
        }
    )

   
    
    # ?? grafico 2
    #?? =====================================================================
    col_nivel = "Nivel De Interes"

    counts = filtered_df[col_nivel].dropna().value_counts().reset_index()
    counts.columns = [col_nivel, "Porcentaje"]
    counts["Porcentaje"] = (counts["Porcentaje"] /
                            counts["Porcentaje"].sum()) * 100

    fig2 = px.bar(
        counts,
        x=col_nivel,
        y="Porcentaje",
        text=counts["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
        title="Nivel de Interés (% del total)",
        labels={col_nivel: "Nivel de Interés",
                "Porcentaje": "Porcentaje del total"}
    )

    fig2.update_traces(textposition="outside")
    fig2.update_layout(yaxis_title="Porcentaje", xaxis_title="Nivel de Interés")

 
    # ?? grafico 3
    # ?? =====================================================================
    
    col_proj = "Proyectos Relacionados"
    col_nivel = "Nivel De Interes"
    base = filtered_df[[col_proj, col_nivel]].dropna()


    tab = (
        base.groupby([col_proj, col_nivel])
        .size()
        .reset_index(name="Cantidad")
    )

    fig3 = px.bar(
        tab,
        x=col_proj,
        y="Cantidad",
        color=col_nivel,
        barmode="stack",
        title="Proyectos vs Nivel de Interés (Conteos)",
        labels={
            col_proj: "Proyectos Relacionados",
            "Cantidad": "Cantidad de Leads",
            col_nivel: "Nivel de Interés"
        }
    )

    fig3.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Cantidad",
        xaxis_title="Proyectos Relacionados",
        legend_title="Nivel de Interés"
    )

    
    

    # ?? grafico 4
    # ?? =====================================================================
    col_medio = "Medio De Captacion"

    # --- Preparar datos ---
    counts = (
        filtered_df[col_medio]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .reset_index()
    )
    counts.columns = [col_medio, "Cantidad"]

    fig4 = px.bar(
        # ordenado de menor a mayor
        counts.sort_values("Cantidad", ascending=True),
        x="Cantidad",
        y=col_medio,
        orientation="h",  # barras horizontales
        text="Cantidad",
        title="Leads por Medio de Captación",
        labels={
            col_medio: "Medio de Captación",
            "Cantidad": "Cantidad de Leads"
        },
        color="Cantidad",
        color_continuous_scale="Blues"  # paleta de color azul
    )

    fig4.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Cantidad: %{x}<extra></extra>"
    )

    fig4.update_layout(
        xaxis_title="Cantidad de Leads",
        yaxis_title="Medio de Captación",
        coloraxis_showscale=False,
        margin=dict(l=100, r=40, t=60, b=60)
    )
    render_4charts([fig1, fig2, fig3, fig4])




# --- TAB: Áreas más y menos valoradas ---
elif tab_selection == "Áreas más y menos valoradas":
    
    # ?? grafico 5
    # ?? =====================================================================
    st.header("Áreas más y menos valoradas")

    date_col = "Fecha Creación"
    hue = "Nivel De Interes"

    # --- Preparar datos ---
    tmp = filtered_df[[date_col, hue]].dropna().copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
    tmp = tmp.dropna(subset=[date_col])
    tmp["mes"] = tmp[date_col].dt.to_period("M").dt.to_timestamp()

    # Agrupar datos
    tab = (
        tmp.groupby(["mes", hue])
        .size()
        .reset_index(name="Cantidad")
    )

    fig5 = px.area(
        tab,
        x="mes",
        y="Cantidad",
        color=hue,
        title=f"Leads por Mes y {hue}",
        labels={
            "mes": "Mes",
            "Cantidad": "Cantidad de Leads",
            hue: "Nivel de Interés"
        },
        line_group=hue
    )

    fig5.update_layout(
        xaxis_title="Mes",
        yaxis_title="Cantidad de Leads",
        legend_title="Nivel de Interés",
        hovermode="x unified",
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    # ?? grafico 6
    # ?? =====================================================================

    for c in ["Estado Civil", "Proyectos Relacionados"]:
        if c in filtered_df.columns:
            filtered_df[c] = (
                filtered_df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA})
            )


    TOP_PROYECTOS = 8             # número de proyectos principales a mostrar
    MIN_CATEGORIAS_ESTADO = 3     # cantidad mínima de categorías de estado civil a incluir


    top_proy = (
        filtered_df["Proyectos Relacionados"]
        .dropna()
        .value_counts()
        .head(TOP_PROYECTOS)
        .index
    )

    # === Filtrar solo los proyectos seleccionados ===
    sub = filtered_df[filtered_df["Proyectos Relacionados"].isin(top_proy)].copy()

    # === Crear tabla agrupada ===
    tab = (
        sub.groupby(["Proyectos Relacionados", "Estado Civil"])
        .size()
        .reset_index(name="Número de Leads")
    )

# === Filtrar categorías de estado civil menos frecuentes ===
    estado_counts = tab["Estado Civil"].value_counts().head(
        MIN_CATEGORIAS_ESTADO).index
    tab = tab[tab["Estado Civil"].isin(estado_counts)]



    fig6 = px.bar(
        tab,
        x="Proyectos Relacionados",
        y="Número de Leads",
        color="Estado Civil",
        barmode="group",  # barras agrupadas
        title="Estado Civil vs Proyecto",
        labels={
            "Proyectos Relacionados": "Proyecto",
            "Número de Leads": "Número de Leads",
            "Estado Civil": "Estado Civil"
        },
    )

    fig6.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Proyecto",
        yaxis_title="Número de Leads",
        legend_title="Estado Civil",
        margin=dict(l=60, r=40, t=60, b=60)
    )

    # ?? grafico 7
    # ?? =====================================================================

    for c in ["Área Social más valorada", "Nivel De Interes"]:
        if c in filtered_df.columns:
            filtered_df[c] = (
                filtered_df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA})
            )

    # === Parámetros ===
    TOP_GUSTOS = 8 

    # === Seleccionar las áreas sociales más valoradas (top N)
    top_gustos = (
    filtered_df["Área Social más valorada"]
    .dropna()
    .value_counts()
    .head(TOP_GUSTOS)
    .index
    )

    # === Filtrar solo los registros del top ===
    sub = filtered_df[filtered_df["Área Social más valorada"].isin(top_gustos)].copy()

    # === Crear tabla agrupada ===
    tab = (
    sub.groupby(["Área Social más valorada", "Nivel De Interes"])
    .size()
    .reset_index(name="Número de Leads")
    )

  
    fig7 = px.bar(
    tab,
    x="Área Social más valorada",
    y="Número de Leads",
    color="Nivel De Interes",
    barmode="group",  # barras agrupadas por nivel de interés
    title="Gusto del Cliente vs Nivel de Interés",
    labels={
        "Área Social más valorada": "Área Social Más Valorada",
        "Número de Leads": "Número de Leads",
        "Nivel De Interes": "Nivel de Interés"
    },
    )

    fig7.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Área Social Más Valorada",
    yaxis_title="Número de Leads",
    legend_title="Nivel de Interés",
    margin=dict(l=60, r=40, t=60, b=60)
    )

    # ?? grafico 8
    # ?? =====================================================================
    for c in ["Usuario Creador", "Proyectos Relacionados"]:
        if c in filtered_df.columns:
            filtered_df[c] = (
                filtered_df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA, "no": pd.NA})
            )

    filtered_df = filtered_df.dropna(subset=["Usuario Creador", "Proyectos Relacionados"])

    # === Parámetros ===
    TOP_ASESORES = 6
    TOP_PROYECTOS = 5


    top_asesores = filtered_df["Usuario Creador"].value_counts().head(TOP_ASESORES).index
    sub = filtered_df[filtered_df["Usuario Creador"].isin(top_asesores)].copy()

    # === Agrupar proyectos pequeños como "otros proyectos" ===
    conteo_proy = sub["Proyectos Relacionados"].value_counts()
    proy_principales = conteo_proy.head(TOP_PROYECTOS).index

    sub["Proyecto Simplificado"] = np.where(
        sub["Proyectos Relacionados"].isin(proy_principales),
        sub["Proyectos Relacionados"],
        "otros proyectos"
    )

    # === Calcular porcentaje de leads por asesor y proyecto ===
    tab = (
        sub.groupby(["Usuario Creador", "Proyecto Simplificado"])
        .size()
        .reset_index(name="Cantidad")
    )

    tab_total = tab.groupby("Usuario Creador")["Cantidad"].transform("sum")
    tab["Porcentaje"] = (tab["Cantidad"] / tab_total) * 100

  
    fig8 = px.bar(
        tab,
        y="Usuario Creador",
        x="Porcentaje",
        color="Proyecto Simplificado",
        orientation="h",  # barras horizontales
        title="Distribución de proyectos por asesor — Top asesores (agrupado)",
        labels={
            "Usuario Creador": "Asesor (Top por volumen)",
            "Proyecto Simplificado": "Proyecto",
            "Porcentaje": "% de Leads por Proyecto"
        },
        text=tab["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig8.update_traces(textposition="inside", insidetextanchor="middle")
    fig8.update_layout(
        xaxis_title="% de Leads por Proyecto",
        yaxis_title="Asesor",
        legend_title="Proyecto",
        xaxis=dict(tickformat=".0f"),
        barmode="stack",
        margin=dict(l=80, r=40, t=60, b=60)
    )


    render_4charts([fig5, fig6, fig7, fig8])


# --- TAB: Nivel de Interés ---
elif tab_selection == "Nivel de Interés":
    st.header("Nivel de Interés")
    
    #? grafico 9
    #? =====================================================================

    col_nivel = "Nivel De Interes"
    col_financiamiento = "Tipo de Financiamiento"

    # Filtrar valores nulos
    df_filtrado = filtered_df[[col_financiamiento, col_nivel]].dropna()

    # Contar proyectos relacionados por Tipo de Financiamiento y Nivel de Interés
    conteo_todos = (
        df_filtrado
        .groupby([col_financiamiento, col_nivel])
        .size()
        .reset_index(name="Proyectos Relacionados")
    )

    # Crear gráfico interactivo con Plotly
    fig9 = px.bar(
        conteo_todos,
        x=col_financiamiento,
        y="Proyectos Relacionados",
        color=col_nivel,
        barmode="group",  # puedes cambiar a "stack" si prefieres apilado
        text="Proyectos Relacionados",
        title="Todos los Tipos de Financiamiento",
        labels={
            col_financiamiento: "Tipo de Financiamiento",
            "Proyectos Relacionados": "Número de Proyectos Relacionados",
            col_nivel: "Nivel de Interés"
        },
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig9.update_traces(textposition="outside")  # mostrar valores sobre las barras
    fig9.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Tipo de Financiamiento",
        yaxis_title="Número de Proyectos Relacionados",
        legend_title="Nivel de Interés",
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )



    #? grafico 10
    #? =====================================================================

    col_area = "Área Social más valorada"
    col_nivel = "Nivel De Interes"


    # Filtrar valores nulos
    df_filtrado = filtered_df[[col_area, col_nivel, "Proyectos Relacionados"]].dropna()

    # Agrupar para gráfico agrupado
    conteo = (
        df_filtrado
        .groupby([col_area, col_nivel])["Proyectos Relacionados"]
        .count()
        .reset_index()
    )

    # =============================
    # Gráfico de barras horizontal agrupado
    # =============================
    fig10 = px.bar(
        conteo,
        y=col_area,
        x="Proyectos Relacionados",
        color=col_nivel,
        barmode="group",
        text="Proyectos Relacionados",
        orientation="h",
        title="Proyectos Relacionados según Áreas Comunes y Nivel de Interés (Agrupado)",
        labels={
            col_area: "Áreas Comunes Valoradas",
            "Proyectos Relacionados": "Número de Proyectos Relacionados",
            col_nivel: "Nivel de Interés"
        },
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig10.update_traces(textposition="outside")
    

    # =============================
    # Gráfico de barras horizontal apilado
    # =============================
    fig10 = px.bar(
        conteo,
        y=col_area,
        x="Proyectos Relacionados",
        color=col_nivel,
        barmode="stack",
        text="Proyectos Relacionados",
        orientation="h",
        title="Proyectos Relacionados según Áreas Comunes y Nivel de Interés (Apilado)",
        labels={
            col_area: "Áreas Comunes Valoradas",
            "Proyectos Relacionados": "Número de Proyectos Relacionados",
            col_nivel: "Nivel de Interés"
        },
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig10.update_traces(textposition="inside")

   

    #? grafico 11
    #? =====================================================================

    col_area = "Área Social más valorada"


    # # Mostrar las áreas sociales disponibles
    # st.write("Áreas encontradas en el dataset:")
    # st.write(filtered_df[col_area].dropna().unique())

    # Agrupar por área social y contar proyectos relacionados
    conteo_proyectos = (
        filtered_df.groupby(col_area)["Proyectos Relacionados"]
        .count()
        .reset_index()
        .rename(columns={"Proyectos Relacionados": "Cantidad de Proyectos"})
        .sort_values("Cantidad de Proyectos", ascending=True)
    )

    # Crear gráfico de barras horizontal interactivo
    fig11 = px.bar(
        conteo_proyectos,
        y=col_area,
        x="Cantidad de Proyectos",
        orientation="h",
        text="Cantidad de Proyectos",
        title="Áreas Sociales más valoradas vs Número de Proyectos Relacionados",
        labels={
            col_area: "Área Social más valorada",
            "Cantidad de Proyectos": "Cantidad de Proyectos Relacionados"
        },
        color="Cantidad de Proyectos",
        color_continuous_scale="Blues"  # similar al color 'skyblue' original
    )

    # Personalizar visualización
    fig11.update_traces(textposition="outside")
    fig11.update_layout(
        xaxis_title="Cantidad de Proyectos Relacionados",
        yaxis_title="Área Social más valorada",
        coloraxis_showscale=False,
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )


    
    
    #? grafico 12
    #? =====================================================================
    col_financiamiento = "Tipo de Financiamiento"
    col_interes = "Nivel De Interes"
    col_genero = "Genero"

    # Agrupamos por Tipo de Financiamiento, Nivel de Interes y Genero
    conteo_nivel_ingresos = (
        filtered_df.groupby([col_financiamiento, col_interes, col_genero])
        .size()
        .reset_index(name="Cantidad")
    )

    # Creamos la columna combinada "Grupo"
    conteo_nivel_ingresos["Grupo"] = (
        conteo_nivel_ingresos[col_genero].astype(str)
        + " - "
        + conteo_nivel_ingresos[col_interes].astype(str)
    )

    # Gráfico con Plotly Express
    fig12 = px.bar(
        conteo_nivel_ingresos,
        x=col_financiamiento,
        y="Cantidad",
        color="Grupo",
        barmode="group",
        title="Distribución de Tipo de Financiamiento vs Nivel de Interés por Género",
        labels={
            col_financiamiento: "Tipo de Financiamiento",
            "Cantidad": "Cantidad de Personas",
            "Grupo": "Género + Nivel de Interés",
        },
    )

    # Ajustes visuales
    fig12.update_layout(
        xaxis_title="Tipo de Financiamiento",
        yaxis_title="Cantidad de Personas",
        legend_title="Género + Nivel de Interés",
        xaxis_tickangle=-45,
    )


    render_4charts([fig9, fig10, fig11, fig12])


