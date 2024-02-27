import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.title('Distribuição Normal')
st.write('A distribuição normal é uma das mais importantes distribuições de probabilidade. Ela é uma distribuição contínua, simétrica em relação à média, em forma de sino, e é caracterizada pelos seus dois parâmetros: a média (μ) e o desvio padrão (σ).')
st.caption('Desenvolvido pelo Prof. Matheus C. Pestana (FGV ECMI)')
col1, col2 = st.columns([1, 2])
col1.header('Medidas')
gera_med = col1.button('Gerar Medidas aleatórias')
tipo = col1.radio('Escolha o tipo de medida', ['Altura', 'Idade'])
alturas = []
if gera_med:
    if tipo == 'Altura':
        alturas = np.random.normal(1.70, 0.1, 15)
        alturas = np.round(alturas, 2)
    else:
        alturas = np.random.normal(20, 3, 15)
        alturas = np.round(alturas, 0)
ids = range(1, 16, 1)
df_alturas = pd.DataFrame(ids, columns=['Aluno'])
if len(alturas) > 1:
    df_alturas['Medida'] = alturas
else:
    df_alturas['Medida'] = 0
alturas = col1.data_editor(df_alturas)

col2.header('Distribuição de Medidas')
df = pd.DataFrame({'Medida': alturas['Medida']})
col2.write(alt.Chart(df).mark_bar().encode(x=alt.X('Medida', bin=True), y='count()').properties(width=600, height=600))
