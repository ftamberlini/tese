import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    layout = "wide",
    page_title = "Dados de Filmes x Gênero"
)

@st.cache_data
def load_data():
    df = pd.read_csv("filmes.csv",converters={'TITULO':str},sep=";;")
    return df

df = load_data()
st.session_state["df_filmes"]= df

scale = alt.Scale(
    domain = ["M","F"],
    range=["#0066ff","#ff99cc"]
)
color = alt.Color("DIRETOR_GENERO:N",scale=scale)
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])

points = (
    alt.Chart(df)
    .mark_point()
    .encode(
        alt.X("NOTA",title="Nota IMDB"),
        alt.Y("VOTOS",title="Votos IMDB"),
        color=alt.condition(brush, color, alt.value("lightgray")),
        size="QTD_PUBLICO",
        tooltip=["TITULO","PAIS_OBRA"],
    )
    .properties(width=550,height=300)
    .add_selection(brush)
    .transform_filter(click)
)

bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="PAIS_OBRA:N",
        color=alt.condition(click, color, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .add_selection(click)
    )
chart = alt.vconcat(points,bars,data=df, title="Filmes por Gênero de Diretor")

tab1, tab2 = st.tabs(["Modelo 1", "Modelo 2"])

with tab1:
    st.altair_chart(chart,theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(chart,theme=None, use_container_width=True)
