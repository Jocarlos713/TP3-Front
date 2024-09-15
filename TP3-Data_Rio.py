import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar e tratar o arquivo CSV para o dashboard (tratamento específico)
def carregar_e_tratar_dados():
    df = pd.read_excel('2675.xls', sheet_name= '2019', skiprows=5).iloc[:102]
    df = df.drop([0, 1])
    df = df.drop(columns=['Total'])
    df = df.rename(columns={"Unnamed: 0": 'Países'})
    continentes = ["África", "América Central", "América do Norte", "América do Sul", "Ásia", "Europa", "Oceania", "Oriente Médio"]
    df = df[~df['Países'].isin(continentes)]
    
    # Converter colunas numéricas (todas as colunas exceto a primeira)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Página do dashboard
def pagina_dashboard():
    st.title("Dashboard de Dados de Turismo")

    # Carregar e tratar os dados para o dashboard
    df = carregar_e_tratar_dados()

    # Exibir o dataframe
    st.subheader("Tabela de Dados")
    st.dataframe(df)

    # Top 5 países com mais visitas
    st.subheader("5 Países com Mais Visitas")
    
    # Somar os valores de visitas em todas as colunas (de cada país) e pegar os 5 maiores
    df['Total_Visitas'] = df.iloc[:, 1:].sum(axis=1)
    top5_paises = df.nlargest(5, 'Total_Visitas')

    fig1, ax1 = plt.subplots()
    ax1.pie(top5_paises['Total_Visitas'], labels=top5_paises['Países'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Gráfico de pizza em formato circular
    st.pyplot(fig1)

    # Selecionar um país e mostrar gráfico de visitas ao longo dos meses
    st.subheader("Selecione um País para Visualizar as Visitas ao Longo dos Meses")
    paises_disponiveis = df['Países'].unique()
    pais_selecionado = st.selectbox("Escolha o país", paises_disponiveis)

    # Mostrar gráfico de linha para o país selecionado
    df_pais = df[df['Países'] == pais_selecionado]
    fig2, ax2 = plt.subplots()
    ax2.plot(df.columns[1:-1], df_pais.iloc[0, 1:-1], marker='o')
    ax2.set_title(f'Visitas ao longo dos meses para {pais_selecionado}')
    ax2.set_xlabel('Meses')
    ax2.set_ylabel('Número de Visitas')
    st.pyplot(fig2)

# Interface de navegação entre páginas
def main():
    # Abas para navegação entre páginas
    aba = st.sidebar.radio("Navegue pelas páginas", ["Upload de Arquivo CSV", "Dashboard de Turismo"])

    if aba == "Dashboard de Turismo":
        pagina_dashboard()

if __name__ == '__main__':
    main()
