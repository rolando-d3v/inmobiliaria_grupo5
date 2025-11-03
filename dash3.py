import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Ejercicio 3",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Titanic Dataset Analysis EDA")
st.markdown("Explore the titanic dataset")


# Importando el dataset de titanic
data = sns.load_dataset("titanic")

data["age"] = data["age"].fillna(data["age"].median())
data["fare"] = data["fare"].fillna(data["fare"].median())

# Agrupar la edad en grupos etarios

bins = [0, 12, 20, 30, 50, 100]
labels = ["Child", "Teen", "Young adult", "Adult", "Senior"]
data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels)


st.sidebar.header("Controles")
char_type = st.sidebar.selectbox(
    "Selecciona el tipo de visualizacion",
    [
        "Resumen de supervivencia",
        "Grafico demografico",
        "Analisis de tarifas",
        "Relacion familiar",
    ],
)

st.sidebar.markdown("## Filtros")
selected_class = st.sidebar.multiselect(
    "Clase de pasajero",
    options=data["class"].unique(),
    default=data["class"].unique(),
)

selected_sex = st.sidebar.multiselect(
    "Sexo",
    options=data["sex"].unique(),
    default=data["sex"].unique(),
)

filtered_df = data[
    (data["class"].isin(selected_class)) & (data["sex"].isin(selected_sex))
]

st.write(filtered_df)


st.subheader(f"Visualizacion de {char_type}")

if char_type == "Resumen de supervivencia":
    col1, col2 = st.columns(2)

    with col1:
        st.write("Resumen de supervivencia por clase")
        survived_class = filtered_df.groupby("class")["survived"].mean().reset_index()
        fig = px.bar(survived_class, x="class", y="survived")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("Resumen de supervivencia por sexo")
        survived_by_gender = filtered_df.groupby("sex")["survived"].mean().reset_index()
        fig = px.pie(survived_by_gender, values="survived", names="sex")
        st.plotly_chart(fig, use_container_width=True)


elif char_type == "Grafico demografico":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Grafico de distribucion de edad")
        fig = px.histogram(filtered_df, x="age", nbins=20)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("Grafico de distribucion de tarifas")
        fig = px.pie(filtered_df, names="class", title="Passenger Class Distribution")
        st.plotly_chart(fig, use_container_width=True)

elif char_type == "Analisis de tarifas":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Grafico de distribucion de tarifas")
        fig = px.histogram(filtered_df, x="fare", nbins=20)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("Grafico de distribucion de tarifas")
        fig = px.pie(filtered_df, names="class", title="Passenger Class Distribution")
        st.plotly_chart(fig, use_container_width=True)


elif char_type == "Relacion familiar":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Familia cercana vs Muerte")
        sib = filtered_df.groupby("sibsp")["survived"].mean().reset_index()
        fig = px.bar(sib, x="sibsp", y="survived")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("Familias/ Hijos vs Sobrevivencia")
        parch = filtered_df.groupby("parch")["survived"].mean().reset_index()
        fig = px.bar(parch, x="parch", y="survived")
        st.plotly_chart(fig, use_container_width=True)