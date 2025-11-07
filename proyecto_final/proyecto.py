import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import unicodedata
import re

# --- Título ---
st.title("Dashboard Inmobiliaria")

# --- Cargar datos ---
df = pd.read_csv("./data_limpia_inmobiliaria.csv")
df["Fecha Creación"] = pd.to_datetime(df["Fecha Creación"])

# --- Controles de selección ---
st.sidebar.header("Controles")
chart_type = st.sidebar.selectbox(
    "Selecciona el tipo de gráfico",
    [
        {"id": 1, "name": "1️ Mascotas vs Nivel de Interés"},
        {"id": 2, "name": "2️ Nivel de Interés (%)"},
        {"id": 3, "name": "3️ Proyectos vs Nivel de Interés"},
        {"id": 4, "name": "4️ Leads por Medio de Captación"},
        {"id": 5, "name": "5️ Leads por Mes y Nivel de Interés"},
        {"id": 6, "name": "6️ Estado Civil vs Proyecto"},
        {"id": 7, "name": "7️ Gusto del Cliente vs Nivel de Interés"},
        {"id": 8, "name": "8️ Distribución de proyectos por asesor — Top asesores (agrupado)"},
        {"id": 9, "name": "9️ Todos los Tipos de Financiamiento" },
        {"id": 10, "name": "10️ Área Social más valorada vs Nivel de Interés" },
        {"id": 11, "name": "11️ Área Social más valorada vs Número de Proyectos Relacionados" },
        {"id": 12, "name": "12️ Nivel de Ingresos VS Nivel de Interés en base al perfil del cliente" },
        {"id": 13, "name": "13️ Canal de Entrada VS Nivel de Interés en base al perfil del cliente" }
    
    ],
    format_func=lambda option: option["name"]
)





# ?? 1 Gráfico: Mascotas vs Nivel de Interés
# =======================================================================
if chart_type["id"] == 1:
    niveles_seleccionados = ['compró', 'alto', 'medio', 'bajo']
    df_filtrado = df[df['Nivel De Interes'].isin(niveles_seleccionados)]

    tabla_mascotas = (
        df_filtrado.groupby(["Tiene mascotas (si,no)", "Nivel De Interes"])
        .size()
        .reset_index(name="Número de Leads")
    )

    fig = px.bar(
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

    st.plotly_chart(fig, use_container_width=True)

# ?? 2️ Gráfico: Nivel de Interés (%)
# =======================================================================
elif chart_type["id"] == 2:
    col_nivel = "Nivel De Interes"

    counts = df[col_nivel].dropna().value_counts().reset_index()
    counts.columns = [col_nivel, "Porcentaje"]
    counts["Porcentaje"] = (counts["Porcentaje"] /
                            counts["Porcentaje"].sum()) * 100

    fig = px.bar(
        counts,
        x=col_nivel,
        y="Porcentaje",
        text=counts["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
        title="Nivel de Interés (% del total)",
        labels={col_nivel: "Nivel de Interés",
                "Porcentaje": "Porcentaje del total"}
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_title="Porcentaje", xaxis_title="Nivel de Interés")

    st.plotly_chart(fig, use_container_width=True)


# ?? 3️ Gráfico: Proyectos vs Nivel de Interés
# =======================================================================
elif chart_type["id"] == 3:
    col_proj = "Proyectos Relacionados"
    col_nivel = "Nivel De Interes"

    base = df[[col_proj, col_nivel]].dropna()

    # Agrupar y contar
    tab = (
        base.groupby([col_proj, col_nivel])
        .size()
        .reset_index(name="Cantidad")
    )

    # --- Crear gráfico interactivo con Plotly ---
    st.subheader("Proyectos vs Nivel de Interés (Conteos)")

    fig = px.bar(
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

    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Cantidad",
        xaxis_title="Proyectos Relacionados",
        legend_title="Nivel de Interés"
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)



# ?? 4️ Gráfico: Leads por Medio de Captación
# =======================================================================
elif chart_type["id"] == 4:
    col_medio = "Medio De Captacion"

    # --- Preparar datos ---
    counts = (
        df[col_medio]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .reset_index()
    )
    counts.columns = [col_medio, "Cantidad"]

    # --- Crear gráfico interactivo con Plotly ---
    st.subheader("Leads por Medio de Captación")

    fig = px.bar(
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

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Cantidad: %{x}<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Cantidad de Leads",
        yaxis_title="Medio de Captación",
        coloraxis_showscale=False,
        margin=dict(l=100, r=40, t=60, b=60)
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)


# ?? 5️ Gráfico: Leads por Mes y Nivel de Interés
# =======================================================================
elif chart_type["id"] == 5:
    date_col = "Fecha Creación"
    hue = "Nivel De Interes"

    # --- Preparar datos ---
    tmp = df[[date_col, hue]].dropna().copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
    tmp = tmp.dropna(subset=[date_col])
    tmp["mes"] = tmp[date_col].dt.to_period("M").dt.to_timestamp()

    # Agrupar datos
    tab = (
        tmp.groupby(["mes", hue])
        .size()
        .reset_index(name="Cantidad")
    )

    # --- Crear gráfico interactivo con Plotly ---
    st.subheader("Leads por Mes y Nivel de Interés")

    fig = px.area(
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

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Cantidad de Leads",
        legend_title="Nivel de Interés",
        hovermode="x unified",
        margin=dict(l=60, r=40, t=60, b=60)
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)


# ?? 6️ Gráfico: Estado Civil vs Proyecto
# =======================================================================
elif chart_type["id"] == 6:
    # === Normalización de columnas ===
    for c in ["Estado Civil", "Proyectos Relacionados"]:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA})
            )


    TOP_PROYECTOS = 8             # número de proyectos principales a mostrar
    MIN_CATEGORIAS_ESTADO = 3     # cantidad mínima de categorías de estado civil a incluir

# === Seleccionar los proyectos con más leads ===
    top_proy = (
        df["Proyectos Relacionados"]
        .dropna()
        .value_counts()
        .head(TOP_PROYECTOS)
        .index
    )

    # === Filtrar solo los proyectos seleccionados ===
    sub = df[df["Proyectos Relacionados"].isin(top_proy)].copy()

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

# === Gráfico interactivo con Plotly ===
    st.subheader("Estado Civil vs Proyecto (Interactivo)")

    fig = px.bar(
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

    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Proyecto",
        yaxis_title="Número de Leads",
        legend_title="Estado Civil",
        margin=dict(l=60, r=40, t=60, b=60)
    )


    st.plotly_chart(fig, use_container_width=True)


# ?? 7️ Gráfico: Gusto del Cliente vs Nivel de Interés
# =======================================================================
elif chart_type["id"] == 7:
    for c in ["Área Social más valorada", "Nivel De Interes"]:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA})
            )

    # === Parámetros ===
    TOP_GUSTOS = 8  # Número de gustos principales a mostrar

    # === Seleccionar las áreas sociales más valoradas (top N) ===
    top_gustos = (
    df["Área Social más valorada"]
    .dropna()
    .value_counts()
    .head(TOP_GUSTOS)
    .index
    )

    # === Filtrar solo los registros del top ===
    sub = df[df["Área Social más valorada"].isin(top_gustos)].copy()

    # === Crear tabla agrupada ===
    tab = (
    sub.groupby(["Área Social más valorada", "Nivel De Interes"])
    .size()
    .reset_index(name="Número de Leads")
    )

    # === Crear gráfico interactivo con Plotly ===
    st.subheader("Gusto del Cliente vs Nivel de Interés")

    fig = px.bar(
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

    fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Área Social Más Valorada",
    yaxis_title="Número de Leads",
    legend_title="Nivel de Interés",
    margin=dict(l=60, r=40, t=60, b=60)
    )

    # === Mostrar en Streamlit ===
    st.plotly_chart(fig, use_container_width=True)


# ?? 8️ Gráfico: Distribución de proyectos por asesor — Top asesores (agrupado)
# =======================================================================
elif chart_type["id"] == 8:
    for c in ["Usuario Creador", "Proyectos Relacionados"]:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"nan": pd.NA, "no": pd.NA})
            )

    df = df.dropna(subset=["Usuario Creador", "Proyectos Relacionados"])

    # === Parámetros ===
    TOP_ASESORES = 6
    TOP_PROYECTOS = 5

    # === Seleccionar los asesores top ===
    top_asesores = df["Usuario Creador"].value_counts().head(TOP_ASESORES).index
    sub = df[df["Usuario Creador"].isin(top_asesores)].copy()

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

    # === Crear gráfico interactivo con Plotly ===
    st.subheader("Distribución de proyectos por asesor — Top asesores (agrupado)")

    fig = px.bar(
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

    fig.update_traces(textposition="inside", insidetextanchor="middle")
    fig.update_layout(
        xaxis_title="% de Leads por Proyecto",
        yaxis_title="Asesor",
        legend_title="Proyecto",
        xaxis=dict(tickformat=".0f"),
        barmode="stack",
        margin=dict(l=80, r=40, t=60, b=60)
    )

    # === Mostrar en Streamlit ===
    st.plotly_chart(fig, use_container_width=True)
    
    
# ?? 9️ Gráfico: Todos los Tipos de Financiamiento
# =======================================================================
elif chart_type["id"] == 9:
    col_nivel = "Nivel De Interes"
    col_financiamiento = "Tipo de Financiamiento"

    # Filtrar valores nulos
    df_filtrado = df[[col_financiamiento, col_nivel]].dropna()

    # Contar proyectos relacionados por Tipo de Financiamiento y Nivel de Interés
    conteo_todos = (
        df_filtrado
        .groupby([col_financiamiento, col_nivel])
        .size()
        .reset_index(name="Proyectos Relacionados")
    )

    # Crear gráfico interactivo con Plotly
    fig = px.bar(
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

    fig.update_traces(textposition="outside")  # mostrar valores sobre las barras
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Tipo de Financiamiento",
        yaxis_title="Número de Proyectos Relacionados",
        legend_title="Nivel de Interés",
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)



# ?? 10️ Gráfico: Área Social más valorada vs Nivel de Interés
# =======================================================================
elif chart_type["id"] == 10:
    col_area = "Área Social más valorada"
    col_nivel = "Nivel De Interes"

    st.subheader("Área Común más Valorada vs Nivel de Interés")

    # Filtrar valores nulos
    df_filtrado = df[[col_area, col_nivel, "Proyectos Relacionados"]].dropna()

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
    fig_grouped = px.bar(
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
    fig_grouped.update_traces(textposition="outside")
    st.plotly_chart(fig_grouped, use_container_width=True)

    # =============================
    # Gráfico de barras horizontal apilado
    # =============================
    fig_stacked = px.bar(
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
    fig_stacked.update_traces(textposition="inside")
    st.plotly_chart(fig_stacked, use_container_width=True)


elif chart_type["id"] == 11:
    col_area = "Área Social más valorada"

    st.subheader("Áreas Sociales más valoradas vs Número de Proyectos Relacionados")

    # Mostrar las áreas sociales disponibles
    st.write("Áreas encontradas en el dataset:")
    st.write(df[col_area].dropna().unique())

    # Agrupar por área social y contar proyectos relacionados
    conteo_proyectos = (
        df.groupby(col_area)["Proyectos Relacionados"]
        .count()
        .reset_index()
        .rename(columns={"Proyectos Relacionados": "Cantidad de Proyectos"})
        .sort_values("Cantidad de Proyectos", ascending=True)
    )

    # Crear gráfico de barras horizontal interactivo
    fig = px.bar(
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
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Cantidad de Proyectos Relacionados",
        yaxis_title="Área Social más valorada",
        coloraxis_showscale=False,
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)



elif chart_type["id"] == 12:  # Puedes asignar el ID que desees
    col_financiamiento = "Tipo de Financiamiento"
    col_interes = "Nivel De Interes"
    col_genero = "Genero"

    # Agrupamos por Tipo de Financiamiento, Nivel de Interes y Genero
    conteo_nivel_ingresos = (
        df.groupby([col_financiamiento, col_interes, col_genero])
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
    fig = px.bar(
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
    fig.update_layout(
        xaxis_title="Tipo de Financiamiento",
        yaxis_title="Cantidad de Personas",
        legend_title="Género + Nivel de Interés",
        xaxis_tickangle=-45,
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)


elif chart_type["id"] == 13:  # Gráfico de financiamiento por nivel de interés y género
    col_financiamiento = "Tipo de Financiamiento"
    col_interes = "Nivel De Interes"
    col_genero = "Genero"

    # Limpiar valores nulos
    df = df.dropna(subset=[col_financiamiento, col_interes, col_genero])

    # Agrupar por Tipo de Financiamiento, Nivel de Interes y Genero
    conteo_nivel_ingresos = (
        df.groupby([col_financiamiento, col_interes, col_genero])
        .size()
        .reset_index(name="Cantidad")
    )

    # Calcular porcentaje dentro de cada tipo de financiamiento
    conteo_nivel_ingresos["Porcentaje"] = (
        conteo_nivel_ingresos.groupby(col_financiamiento)["Cantidad"]
        .apply(lambda x: (x / x.sum()) * 100)
        .reset_index(level=0, drop=True)
    )

    # Crear la columna combinada "Grupo"
    conteo_nivel_ingresos["Grupo"] = (
        conteo_nivel_ingresos[col_genero].astype(str)
        + " - "
        + conteo_nivel_ingresos[col_interes].astype(str)
    )

    # Crear gráfico con Plotly Express
    fig = px.bar(
        conteo_nivel_ingresos,
        x=col_financiamiento,
        y="Porcentaje",
        color="Grupo",
        barmode="group",
        text=conteo_nivel_ingresos["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
        title="Distribución del Tipo de Financiamiento vs Nivel de Interés por Género (%)",
        labels={
            col_financiamiento: "Tipo de Financiamiento",
            "Porcentaje": "Porcentaje dentro del Tipo de Financiamiento",
            "Grupo": "Género + Nivel de Interés",
        },
    )

    # Ajustes visuales
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Tipo de Financiamiento",
        yaxis_title="Porcentaje de Personas",
        legend_title="Género + Nivel de Interés",
        xaxis_tickangle=-45,
        yaxis_range=[0, 100],
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
