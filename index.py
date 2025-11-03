import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Data Visualization Dashboard")
st.markdown("Ejemplos de diferentes tipos de graficos con Streamlit")


@st.cache_data
def load_data():
    np.random.seed(42)
    data_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    data = pd.DataFrame(
        {
            "Date": data_range,
            "Value": np.random.randn(len(data_range)).cumsum() + 100,
            "Category": np.random.choice(["A", "B", "C"], len(data_range)),
            "X": np.random.rand(len(data_range)) * 100,
            "Y": np.random.rand(len(data_range)) * 50,
            "Size": np.random.uniform(10, 100, len(data_range)),
        }
    )
    data["Month"] = data["Date"].dt.month_name()
    return data


# Crea un DataFrame (df) con columnas:
df = load_data()

st.sidebar.header("Controls")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    [
        "Line Chart",
        "Bar Chart",
        "Scatter Plot",
        "Histogram",
        "Box Plot",
        "Area Chart",
        "Pie Chart",
    ],
)

st.subheader(f"{chart_type} Visualization")

if chart_type == "Line Chart":
    col1, col2 = st.columns(2)

    with col1:

        st.write("Streamlit Line Chart")
        st.line_chart(data=df, x="Date", y="Value")

    with col2:

        st.write("Altair Interactive Line Chart")
        alt_chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x="Date",
                y="Value",
                color="Category",
                tooltip=["Date", "Value", "Category"],
            )
            .interactive()
        )
        st.altair_chart(alt_chart, use_container_width=True)

elif chart_type == "Bar Chart":
    col1, col2 = st.columns(2)

    with col1:

        st.write("Streamlit Bar Chart")
        st.bar_chart(data=df, x="Date", y="Value")
    with col2:
        st.write("Plotly Interactive Bar Chart")
        fig = px.bar(
            df,
            x="Month",
            y="Value",
            barmode="group",
            color="Category",
            title="Interactive Bar Chart",
        )
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter Plot":
    col1, col2 = st.columns(2)

    with col1:

        st.write("Matplotlib Scatter Plot")
        fig, ax = plt.subplots()
        sns.scatterplot(
            data=df, x="X", y="Y", hue="Category", size="Size", sizes=(20, 200), ax=ax
        )
        ax.set_title("X vs Y by Category")
        st.pyplot(fig)

    with col2:

        st.write("Plotly 3D Scatter Plot")
        fig = px.scatter_3d(
            df,
            x="X",
            y="Y",
            z="Value",
            color="Category",
            size="Size",
            title="3D Scatter Plot",
        )
        st.plotly_chart(fig, use_container_width=True)
elif chart_type == "Histogram":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Streamlit Histogram")
        st.bar_chart(df["Value"])

    with col2:
        st.write("Histograma con Seaborn")
        fig, ax = plt.subplots()
        sns.histplot(data=df, x="Value", hue="Category", ax=ax)
        st.pyplot(fig)
elif chart_type == "Box Plot":
    st.write("Box Plot of Value by Category")
    box_plot = (
        alt.Chart(df).mark_boxplot().encode(x="Category", y="Value", color="Category")
    )
    st.altair_chart(box_plot, use_container_width=True)

elif chart_type == "Pie Chart":
    st.write("Distribution of Categories")
    category_counts = df["Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    fig = px.pie(
        category_counts, values="Count", names="Category", title="Category Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Area Chart":
    st.write("Area Chart of Values Over Time")
    fig = px.area(
        df, x="Date", y="Value", color="Category", title="Values Over Time by Category"
    )
    st.plotly_chart(fig, use_container_width=True)