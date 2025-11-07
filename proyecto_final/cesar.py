
import re
import unicodedata
import pandas as pd
import plotly.express as px


csv_path = "data_limpia_inmobiliaria.csv"   
df = pd.read_csv(csv_path)

# -------------------------
# Normalizamos nombres de columnas (minúsculas, sin tildes, _)
# -------------------------
def normalize(s: str) -> str:
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

df.columns = [normalize(c) for c in df.columns]

# =========================
# 2) Resolver nombres de columnas esperadas
#    (si en el CSV vienen con variantes)
# =========================
# Diccionario: clave lógica -> posibles alias que buscamos
aliases = {
    "usuario_distrito": [
        "usuario_distrito", "distrito_usuario", "distrito", "ubigeo", "distrito_contacto"
    ],
    "proyecto_relacionado": [
        "proyectos_relacionados", "proyecto", "proyecto_asociado", "proyecto_interes"
    ],
    "edad": [
        "edad", "age"
    ],
    "usuario_creador": [
        "usuario_creador", "creador", "owner", "user_owner", "user_creator"
    ],
    "nivel_interes": [
        "nivel_interes", "interes", "nivel_de_interes"
    ],
    "area_social_mas_valorada": [
        "area_social_mas_valorada", "area_social_valorada", "area_valorada",
        "amenidad_mas_valorada", "amenidad"
    ],
}

def pick_column(logical_name: str) -> str:
    """Busca la primera columna del df que matchee algún alias."""
    for cand in aliases.get(logical_name, []):
        if cand in df.columns:
            return cand
    raise KeyError(
        f"No se encontró la columna para '{logical_name}'. "
        f"Revisa nombres en el CSV: {list(df.columns)}"
    )

col_distrito   = pick_column("usuario_distrito")
col_proyecto   = pick_column("proyecto_relacionado")
col_edad       = pick_column("edad")
col_creador    = pick_column("usuario_creador")
col_interes    = pick_column("nivel_interes")
col_area       = pick_column("area_social_mas_valorada")

# ===========================================================
# 3) Funciones auxiliares de gráficos (Plotly)
# ===========================================================
def heatmap_counts(df, row_col, col_col, title, zlabel="conteo"):
    """
    Heatmap de conteos (tabla cruzada).
    """
    ct = pd.crosstab(df[row_col], df[col_col])
    fig = px.imshow(
        ct,
        text_auto=True,
        color_continuous_scale="Blues",
        aspect="auto",
        labels=dict(color=zlabel, x=col_col, y=row_col),
        title=title
    )
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig

def stacked_bar_norm(df, x_col, color_col, title, barmode="relative", barnorm="percent"):
    """
    Barras apiladas (normalizadas en %) por categoría.
    """
    fig = px.histogram(
        df, x=x_col, color=color_col,
        barmode=barmode, barnorm=barnorm,
        text_auto=True,
        title=title
    )
    fig.update_layout(xaxis_title=x_col, yaxis_title="%", margin=dict(l=40, r=20, t=60, b=40))
    return fig

def box_by_category(df, x_cat, y_num, title):
    """
    Boxplot numérico por categoría, con puntos.
    """
    fig = px.box(
        df, x=x_cat, y=y_num, points="all",
        color=x_cat,
        title=title
    )
    fig.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))
    return fig

# ===========================================================
# 4) GRÁFICOS SOLICITADOS
# ===========================================================

# ---- (1) usuario_distrito vs proyecto_relacionado -> Heatmap + Barras apiladas
fig1a = heatmap_counts(
    df, row_col=col_distrito, col_col=col_proyecto,
    title="Usuarios por Distrito vs Proyecto Relacionado", zlabel="n"
)
fig1a.show()

fig1b = stacked_bar_norm(
    df, x_col=col_distrito, color_col=col_proyecto,
    title="Distribución de Proyecto por Distrito ( % )"
)
fig1b.show()

# ---- (2) proyecto_relacionado vs edad -> Boxplot 
df_num = df.copy()
df_num[col_edad] = pd.to_numeric(df_num[col_edad], errors="coerce")
df_num = df_num.dropna(subset=[col_edad, col_proyecto])

fig2 = box_by_category(
    df_num, x_cat=col_proyecto, y_num=col_edad,
    title="Distribución de Edad por Proyecto Relacionado"
)
fig2.show()

# ---- (3) usuario_creador vs proyecto_relacionado -> Heatmap + Barras apiladas
fig3a = heatmap_counts(
    df, row_col=col_creador, col_col=col_proyecto,
    title="Usuario Creador vs Proyecto Relacionado", zlabel="n"
)
fig3a.show()

fig3b = stacked_bar_norm(
    df, x_col=col_creador, color_col=col_proyecto,
    title="Distribución de Proyectos por Usuario Creador ( % )"
)
fig3b.show()

# ---- (4) usuario_creador vs nivel_interes -> Barras apiladas normalizadas
fig4 = stacked_bar_norm(
    df, x_col=col_creador, color_col=col_interes,
    title="Nivel de Interés por Usuario Creador ( % )"
)
fig4.show()

# ---- (5) area_social_mas_valorada vs proyecto_relacionado -> Heatmap + Barras apiladas
fig5a = heatmap_counts(
    df, row_col=col_area, col_col=col_proyecto,
    title="Área social más valorada vs Proyecto Relacionado", zlabel="n"
)
fig5a.show()

fig5b = stacked_bar_norm(
    df, x_col=col_area, color_col=col_proyecto,
    title="Distribución de Proyectos por Área Social más valorada ( % )"
)
fig5b.show()
