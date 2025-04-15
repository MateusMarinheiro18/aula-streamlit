import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# ✅ DEVE SER O PRIMEIRO COMANDO DE STREAMLIT
st.set_page_config(
    page_title="Dashboard THE SAILOR",
    page_icon="🚢",
    layout="wide"
)

# ========================================
# Paleta de cores inspirada na identidade
# ========================================
color_dark_navy = "#0A1C2E"
color_navy = "#142F43"
color_mid_blue = "#5A7CA5"
color_light_blue = "#A8C2D1"
color_lighter_blue = "#DCE6EF"
color_almost_white = "#EDF3F9"
color_sand = "#C1A57B"
color_gray = "#B8BCC4"

# ========================================
# CSS global (fundo + fonte + metric)
# ========================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {color_almost_white};
        color: {color_dark_navy};
    }}
    .stMetricDelta {{
        color: {color_dark_navy} !important;
    }}
    div[data-testid="metric-container"] {{
        background-color: transparent;
        color: {color_dark_navy};
        border-radius: 8px;
        padding: 8px;
    }}
    div[data-testid="metric-container"] > label {{
        color: {color_dark_navy};
        font-weight: bold;
    }}
    div[data-testid="metric-container"] svg {{
        fill: {color_dark_navy} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========================================
# Leitura dos dados
# ========================================
@st.cache_data
def load_data():
    return pd.read_excel("clientes_loja_perfume_com_gastos_condicionais.xlsx")

df = load_data()

# ========================================
# Título
# ========================================
st.title("Dashboard THE SAILOR - Análise de Vendas")

# ========================================
# Filtros
# ========================================
st.sidebar.header("Filtre os Dados")

sexo_opcoes = df["Sexo"].unique().tolist()
sexo_selecionado = st.sidebar.multiselect("Sexo", sexo_opcoes, default=sexo_opcoes)

faixa_renda_opcoes = df["Faixa de Renda"].unique().tolist()
faixa_renda_selecionado = st.sidebar.multiselect("Faixa de Renda", faixa_renda_opcoes, default=faixa_renda_opcoes)

idade_min = int(df["Idade"].min())
idade_max = int(df["Idade"].max())
idade_selecionada = st.sidebar.slider("Faixa de Idade", idade_min, idade_max, (idade_min, idade_max))

gasto_a_selecionado = st.sidebar.slider(
    "Gasto Produto A (R$)",
    float(df["Gasto Produto A (R$)"].min()),
    float(df["Gasto Produto A (R$)"].max()),
    (float(df["Gasto Produto A (R$)"].min()), float(df["Gasto Produto A (R$)"].max()))
)

gasto_b_selecionado = st.sidebar.slider(
    "Gasto Produto B (R$)",
    float(df["Gasto Produto B (R$)"].min()),
    float(df["Gasto Produto B (R$)"].max()),
    (float(df["Gasto Produto B (R$)"].min()), float(df["Gasto Produto B (R$)"].max()))
)

bairros_opcoes = df["Bairro"].unique().tolist()
bairros_selecionados = st.sidebar.multiselect("Bairro", bairros_opcoes, default=bairros_opcoes)

# ========================================
# Aplicação de filtros
# ========================================
df_filtrado = df[
    (df["Sexo"].isin(sexo_selecionado)) &
    (df["Faixa de Renda"].isin(faixa_renda_selecionado)) &
    (df["Idade"].between(*idade_selecionada)) &
    (df["Gasto Produto A (R$)"].between(*gasto_a_selecionado)) &
    (df["Gasto Produto B (R$)"].between(*gasto_b_selecionado)) &
    (df["Bairro"].isin(bairros_selecionados))
]

# ========================================
# Gráfico 1 – Produto A por Renda
# ========================================
st.subheader("Ticket Médio em Produto A por Faixa de Renda")
ticket_a = df_filtrado.groupby("Faixa de Renda")[["Gasto Produto A (R$)"]].mean().reset_index()

chart1 = alt.Chart(ticket_a).mark_bar(color=color_mid_blue).encode(
    x=alt.X("Faixa de Renda:N", sort=None),
    y=alt.Y("Gasto Produto A (R$):Q")
).properties(
    width=600,
    height=400,
    background='transparent'
).configure_axis(
    labelColor=color_dark_navy,
    titleColor=color_dark_navy
)

st.altair_chart(chart1, use_container_width=True)

# ========================================
# Gráfico 2 – Produto B por Renda
# ========================================
st.subheader("Ticket Médio em Produto B por Faixa de Renda")
ticket_b = df_filtrado.groupby("Faixa de Renda")[["Gasto Produto B (R$)"]].mean().reset_index()

chart2 = alt.Chart(ticket_b).mark_bar(color=color_navy).encode(
    x=alt.X("Faixa de Renda:N", sort=None),
    y=alt.Y("Gasto Produto B (R$):Q")
).properties(
    width=600,
    height=400,
    background='transparent'
).configure_axis(
    labelColor=color_dark_navy,
    titleColor=color_dark_navy
)

st.altair_chart(chart2, use_container_width=True)

# ========================================
# Gráfico 3 – Distribuição de Idade
# ========================================
st.subheader("Distribuição de Idade dos Clientes")
chart3 = alt.Chart(df_filtrado).mark_bar(color=color_dark_navy).encode(
    x=alt.X("Idade:Q", bin=alt.Bin(maxbins=20)),
    y=alt.Y("count():Q", title="Número de Clientes")
).properties(
    width=600,
    height=400,
    background='transparent'
).configure_axis(
    labelColor=color_dark_navy,
    titleColor=color_dark_navy
)

st.altair_chart(chart3, use_container_width=True)

# ========================================
# Métricas com estilo escuro
# ========================================
st.subheader("Totais de Gastos por Produto")
col1, col2 = st.columns(2)
col1.metric("Total Produto A", f"R$ {df_filtrado['Gasto Produto A (R$)'].sum():,.2f}")
col2.metric("Total Produto B", f"R$ {df_filtrado['Gasto Produto B (R$)'].sum():,.2f}")

# ========================================
# Mapa – Compras por Bairro
# ========================================
st.subheader("Distribuição de Compras por Bairro")

neighborhood_coords = {
    "Itaim Bibi": {"lat": -23.6015, "lon": -46.6882},
    "Brooklin": {"lat": -23.6142, "lon": -46.6931},
    "Liberdade": {"lat": -23.5679, "lon": -46.6342},
    "Vila Mariana": {"lat": -23.5981, "lon": -46.6410},
    "Lapa": {"lat": -23.5659, "lon": -46.6685},
}

df_bairros = df_filtrado["Bairro"].value_counts().reset_index()
df_bairros.columns = ["Bairro", "Contagem"]
df_bairros["lat"] = df_bairros["Bairro"].apply(lambda x: neighborhood_coords.get(x, {}).get("lat"))
df_bairros["lon"] = df_bairros["Bairro"].apply(lambda x: neighborhood_coords.get(x, {}).get("lon"))
df_map = df_bairros.dropna(subset=["lat", "lon"])

st.map(df_map)

# ========================================
# Rodapé
# ========================================
st.markdown("---")
st.write("Dashboard desenvolvido para a marca THE SAILOR. Todos os dados são fictícios.")
