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
color1 = alt.Color("DIRETOR_GENERO:N",scale=scale)
color2 = alt.Color("ROTERISTA_GENERO:N",scale=scale)
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])

points1 = (
    alt.Chart(df)
    .mark_point()
    .encode(
        alt.X("NOTA",title="Nota IMDB"),
        alt.Y("VOTOS",title="Votos IMDB"),
        color=alt.condition(brush, color1, alt.value("lightgray")),
        size="QTD_PUBLICO",
        tooltip=["TITULO","PAIS_OBRA"],
    )
    .properties(width=550,height=300)
    .add_selection(brush)
    .transform_filter(click)
)

bars1 = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="PAIS_OBRA:N",
        color=alt.condition(click, color1, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .add_selection(click)
    )
chart1 = alt.vconcat(points1,bars1,data=df, title="Filmes por Gênero Diretor")


points2 = (
    alt.Chart(df)
    .mark_point()
    .encode(
        alt.X("NOTA",title="Nota IMDB"),
        alt.Y("VOTOS",title="Votos IMDB"),
        color=alt.condition(brush, color2, alt.value("lightgray")),
        size="QTD_PUBLICO",
        tooltip=["TITULO","PAIS_OBRA"],
    )
    .properties(width=550,height=300)
    .add_selection(brush)
    .transform_filter(click)
)

bars2 = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="PAIS_OBRA:N",
        color=alt.condition(click, color2, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .add_selection(click)
    )

chart2 = alt.vconcat(points2,bars2,data=df, title="Filmes por Gênero Roterista")

tab1, tab2 = st.tabs(["Gênero Diretor", "Gênero Roterista"])

with tab1:
    st.altair_chart1(chart,theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart2(chart,theme="streamlit", use_container_width=True)
