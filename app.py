import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os

st.set_page_config(page_title="Correlação - FGV ECMI", page_icon="📐", layout="wide")

def main():
    with st.sidebar:
        st.title('Correlação - R de Pearson')
        st.markdown("""
        A presente aplicação tem como objetivo calcular a correlação entre duas variáveis quantitativas, mostrando o funcionamento do índice *r* de Pearson.
        
        Desenvolvida exclusivamente para os alunos do curso de Introdução à Ciência de Dados, da FGV/ECMI, pelo Prof. Matheus C. Pestana.
        """)
        st.subheader('Fórmula')
        st.image('formula.png')

    st.title('FGV/ECMI - Introdução à Ciência de Dados')
    st.header('Correlação - R de Pearson')

    dados = pd.DataFrame({'x': [45, 52, 90, 201, 130, 40, 13, 170, 68, 82, 105],
                          'y': [300, 400, 654, 990, 700, 250, 130, 900, 490, 690, 610]})
    dados = dados.astype(float)

    data_col1, data_col2 = st.columns(2)
    data_col1.header('Dados')
    data_col1.write('Altere abaixo os dados para observar mudanças na correlação.')
    dados = st.experimental_data_editor(dados.rename(columns={'x': 'Variável independente (x)', 'y': 'Variável dependente (y)'}), use_container_width=False)
    dados.rename(columns={'Variável independente (x)': 'x', 'Variável dependente (y)': 'y'}, inplace=True)

    data_col2.metric(label='r de Pearson', value=dados.corr().iloc[1, 0].round(2))

    st.header('Gráfico')
    st.write('Abaixo, é mostrado o gráfico de dispersão entre as variáveis.')
    chart1 = alt.Chart(dados).mark_circle(size=60).encode(x='x', y='y')
    chart2 = chart1 + chart1.transform_regression('x', 'y').mark_line(color='red')
    st.altair_chart(chart1 + chart2, use_container_width=True)


    st.header('Cálculo')
    st.write('Abaixo, é mostrado o cálculo do índice de correlação de Pearson.')
    calc_col1, calc_col2 = st.columns(2)

    calc_col1.subheader('Médias')
    calc_col1.latex(r'Representacão: \bar{x}, \bar{y}')
    calc_col11, calc_col12, calc_col13 = calc_col1.columns(3)
    calc_col11.metric(label='Média de x', value=round(dados['x'].mean(), 2))
    calc_col12.metric(label='Média de y', value=round(dados['y'].mean(), 2))

    dados['x - Md(x)'] = dados['x'] - dados['x'].mean().round(2)
    dados['y - Md(y)'] = dados['y'] - dados['y'].mean().round(2)
    calc_col1.subheader('Diferença entre cada valor e sua média')
    calc_col1.latex(r'Representacão: (x - \bar{x}), (y - \bar{y})')
    calc_col1.dataframe(dados[['x - Md(x)', 'y - Md(y)']], use_container_width=True)

    dados['(x - Md(x)) * (y - Md(y))'] = dados['x - Md(x)'] * dados['y - Md(y)']
    calc_col1.subheader('Produto dessas diferenças')
    calc_col1.latex(r'Representacão: (x - \bar{x}) * (y - \bar{y})')
    calc_col1.dataframe(dados[['(x - Md(x)) * (y - Md(y))']].applymap('{:.2f}'.format), use_container_width=True)

    calc_col1.subheader('Somatório do produto das diferenças')
    calc_col1.latex(r'Representacão: \sum (x - \bar{x})(y - \bar{y})')
    spd = round(dados['(x - Md(x)) * (y - Md(y))'].sum(), 3)
    calc_col1.metric('Resultado', value=spd)

    dados_x2y2 = dados[['x - Md(x)', 'y - Md(y)']].apply(lambda x: x ** 2)
    dados_x2y2 = dados_x2y2.applymap('{:.2f}'.format)
    dados_x2y2.rename(columns={'x - Md(x)': 'x - Md(x)^2', 'y - Md(y)': 'y - Md(y)^2'}, inplace=True)
    calc_col1.subheader('Diferenças ao quadrado')
    calc_col1.latex(r'Representacão: (x - \bar{x})^2, (y - \bar{y})^2')
    calc_col1.dataframe(dados_x2y2[['x - Md(x)^2', 'y - Md(y)^2']], use_container_width=True)

    calc_col1.subheader('Somatório das diferenças ao quadrado')
    calc_col1.latex(r'Representacão: \sum (x - \bar{x})^2, \sum (y - \bar{y})^2')
    calc_col31, calc_col32 = calc_col1.columns(2)
    calc_col31.metric(label='Soma de x-Md(x)^2', value=round(dados_x2y2['x - Md(x)^2'].astype(float).sum(), 2))
    calc_col32.metric(label='Soma de y-Md(y)^2', value=round(dados_x2y2['y - Md(y)^2'].astype(float).sum(), 2))

    calc_col1.subheader('Produto do somatório das diferenças ao quadrado')
    calc_col1.latex(r'Representacão: \sum (x - \bar{x})^2 \sum (y - \bar{y})^2')
    produto_dif = round(dados_x2y2['x - Md(x)^2'].astype(float).sum() * dados_x2y2['y - Md(y)^2'].astype(float).sum(), 2)
    calc_col1.metric(label='Produto das diferenças ao quadrado', value=produto_dif)

    calc_col1.subheader('Raiz do produto do somatório das diferenças ao quadrado')
    calc_col1.latex(r'Representacão: \sqrt{\sum (x - \bar{x})^2 \sum (y - \bar{y})^2}')
    calc_col1.metric(label='Raiz do produto das diferenças ao quadrado', value=round(np.sqrt(produto_dif), 2))

    calc_col1.subheader('Índice de correlação de Pearson')
    calc_col1.latex(r'Representacão: r = \frac{\sum (x - \bar{x})(y - \bar{y})}{\sqrt{\sum (x - \bar{x})^2 \sum (y - \bar{y})^2}}')
    calc_col1.metric(label='r de Pearson', value=round(dados['(x - Md(x)) * (y - Md(y))'].sum() / np.sqrt(produto_dif), 2))

if __name__ == '__main__':
    main()
