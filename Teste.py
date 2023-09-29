import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular o fluxo de caixa
def calcular_fluxo_de_caixa(receitas, custos, despesas, investimentos, depreciação, impostos, crescimento_faturamento):
    fluxo_de_caixa = []

    for i in range(len(receitas)):
        receita = receitas[i]
        custo = custos[i]
        despesa = despesas[i]
        investimento = investimentos[i]
        deprec = depreciação[i]
        imposto = impostos[i]

        lucro_operacional = receita - custo - despesa
        resultado_antes_impostos = lucro_operacional - deprec
        resultado_liquido = resultado_antes_impostos - imposto
        fluxo_de_caixa_operacional = resultado_liquido + deprec
        fluxo_de_caixa_total = fluxo_de_caixa_operacional - investimento

        receitas[i + 1:] *= (1 + crescimento_faturamento)

        fluxo_de_caixa.append(fluxo_de_caixa_total)

    return fluxo_de_caixa

# Interface do Streamlit
def main():
    st.title('Simulador de Fluxo de Caixa para Recuperação Judicial')

    st.sidebar.header('Configurações')

    # Configurações iniciais
    crescimento_faturamento = st.sidebar.slider('Crescimento Anual do Faturamento (%)', min_value=0.0, max_value=10.0, step=0.1, value=0.0)
    anos_simulacao = st.sidebar.slider('Anos de Simulação', min_value=1, max_value=10, step=1, value=5)

    # Dados iniciais
    receitas_iniciais = st.sidebar.number_input('Receitas Iniciais', value=1000000)
    custos_iniciais = st.sidebar.number_input('Custos Iniciais', value=600000)
    despesas_iniciais = st.sidebar.number_input('Despesas Iniciais', value=200000)
    investimentos_iniciais = st.sidebar.number_input('Investimentos Iniciais', value=50000)
    deprec_inicial = st.sidebar.number_input('Depreciação Inicial', value=10000)
    impostos_iniciais = st.sidebar.number_input('Impostos Iniciais', value=50000)

    # Criar o DataFrame base
    df = pd.DataFrame(index=range(anos_simulacao + 1))
    df['Receitas'] = receitas_iniciais
    df['Custos'] = custos_iniciais
    df['Despesas'] = despesas_iniciais
    df['Investimentos'] = investimentos_iniciais
    df['Depreciação'] = deprec_inicial
    df['Impostos'] = impostos_iniciais

    # Calcular o fluxo de caixa
    fluxo_de_caixa = calcular_fluxo_de_caixa(
        df['Receitas'].values,
        df['Custos'].values,
        df['Despesas'].values,
        df['Investimentos'].values,
        df['Depreciação'].values,
        df['Impostos'].values,
        crescimento_faturamento
    )

    df['Fluxo de Caixa'] = fluxo_de_caixa

    # Exibir dados
    st.subheader('Dados de Entrada')
    st.dataframe(df)

    # Gráfico de Fluxo de Caixa
    st.subheader('Gráfico de Fluxo de Caixa')
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Fluxo de Caixa'], marker='o')
    plt.xlabel('Ano')
    plt.ylabel('Fluxo de Caixa')
    st.pyplot(plt)

if __name__ == '__main__':
    main()

