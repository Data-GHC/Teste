import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import numpy_financial as npf

# Função para calcular o fluxo de caixa
def calcular_fluxo_de_caixa(receitas, percentual_custo, percentual_impostos, investimentos, depreciação, impostos_sobre_venda, crescimento_faturamento, pagamentos_rj):
    fluxo_de_caixa = []

    for i in range(len(receitas)):
        receita = receitas[i]
        custo = receita * percentual_custo
        imposto_sobre_venda = receita * percentual_impostos
        investimento = investimentos[i]
        deprec = depreciação[i]
        imposto = impostos_sobre_venda[i]

        lucro_operacional = receita - custo
        resultado_antes_impostos = lucro_operacional - deprec
        resultado_liquido = resultado_antes_impostos - imposto
        fluxo_de_caixa_operacional = resultado_liquido + deprec
        fluxo_de_caixa_total = fluxo_de_caixa_operacional - investimento

        receitas[i + 1:] = receitas[i + 1:].astype('float64') * (1 + crescimento_faturamento)
        
        # Subtrai pagamentos da RJ
        if i < len(pagamentos_rj):
            fluxo_de_caixa_total -= pagamentos_rj[i]

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
    percentual_custo = st.sidebar.slider('Percentual de Custo em relação à Receita (%)', min_value=0, max_value=100, step=1, value=60) / 100
    percentual_impostos = st.sidebar.slider('Percentual de Impostos sobre a Venda (%)', min_value=0, max_value=30, step=1, value=10) / 100
    investimentos_iniciais = st.sidebar.number_input('Investimentos Iniciais', value=50000)
    deprec_inicial = st.sidebar.number_input('Depreciação Inicial', value=10000)
    impostos_iniciais = st.sidebar.number_input('Impostos Iniciais', value=50000)

    # Pagamentos da RJ por classe de credor
    pagamentos_rj = []
    for classe in range(1, 5):
        total_credito = st.sidebar.number_input(f'Total do Crédito Classe {classe}', value=100000)
        desagio_proposto = st.sidebar.slider(f'Deságio Proposto Classe {classe} (%)', min_value=0, max_value=50, step=1, value=20) / 100
        quantidade_parcelas = st.sidebar.number_input(f'Quantidade de Parcelas Classe {classe}', value=12)
        taxa_juros_anual = st.sidebar.slider(f'Taxa de Juros Anual Classe {classe} (%)', min_value=0, max_value=20, step=1, value=5) / 100
    
        taxa_mensal = taxa_juros_anual / 12
        pv = -total_credito * (1 - desagio_proposto)
    
        # Monthly payment calculation
        if taxa_mensal > 0:
            valor_parcela = float(npf.pmt(rate=taxa_mensal, nper=quantidade_parcelas, pv=pv))  # Convertendo para um tipo de dado simples
        else:
            valor_parcela = -pv / quantidade_parcelas
    
        pagamentos_rj += [valor_parcela] * int(quantidade_parcelas)

    # Criar o DataFrame base
    df = pd.DataFrame(index=range(anos_simulacao * 12 + 1))
    df['Receitas'] = receitas_iniciais
    df['Percentual Custo'] = percentual_custo
    df['Percentual Impostos'] = percentual_impostos
    df['Investimentos'] = investimentos_iniciais
    df['Depreciação'] = deprec_inicial
    df['Impostos sobre Venda'] = impostos_iniciais

    # Calcular o fluxo de caixa
    fluxo_de_caixa = calcular_fluxo_de_caixa(
        df['Receitas'].values,
        df['Percentual Custo'].values,
        df['Percentual Impostos'].values,
        df['Investimentos'].values,
        df['Depreciação'].values,
        df['Impostos sobre Venda'].values,
        crescimento_faturamento,
        pagamentos_rj
    )

    df['Fluxo de Caixa'] = fluxo_de_caixa

    # Exibir dados
    st.subheader('Dados de Entrada')
    st.dataframe(df)

    # Gráfico de Fluxo de Caixa
    st.subheader('Gráfico de Fluxo de Caixa')
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Fluxo de Caixa'], marker='o')
    plt.xlabel('Mês')
    plt.ylabel('Fluxo de Caixa')
    st.pyplot(plt)

if __name__ == '__main__':
    main()
