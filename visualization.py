import matplotlib.pyplot as plt
import streamlit as st
from data_loader import carregar_e_tratar_dados
import seaborn as sns

continentes = ["África", "América Central", "América do Norte", "América do Sul", "Ásia", "Europa", "Oceania", "Oriente Médio"]

# Função para exibir o gráfico de pizza com os 5 países com mais visitas
def exibir_grafico_pizza(df):

    # Filtrar para remover os continentes da lista
    df_pizza = df[~df['Países'].isin(continentes)]

    st.subheader("Países com o maior índice de chegadas")

    # Somar os valores de visitas em todas as colunas (de cada país) e pegar os 5 maiores
    df_pizza['Total_Visitas'] = df_pizza.iloc[:, 1:].sum(axis=1)

    # Selecionar os 5 países com mais visitas
    top5_paises = df_pizza.nlargest(5, 'Total_Visitas')

    # Criar o gráfico de pizza
    fig1, ax1 = plt.subplots()
    ax1.pie(top5_paises['Total_Visitas'], labels=top5_paises['Países'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Gráfico de pizza em formato circular

    # Exibir o gráfico
    st.pyplot(fig1)


# Função para exibir o gráfico de linha para um país selecionado
def exibir_grafico_linha(df, pais_selecionado):
    df_pais = df[df['Países'] == pais_selecionado]
    
    fig2, ax2 = plt.subplots()
    ax2.plot(df.columns[1:-1], df_pais.iloc[0, 1:-1], marker='o')
    ax2.set_title(f'Visitas ao longo dos meses para {pais_selecionado}')
    ax2.set_xlabel('Meses')
    ax2.set_ylabel('Número de Visitas')
    st.pyplot(fig2)

# Função para plotar gráfico de linha com a soma de visitas por continente
def exibir_grafico_linha_por_continente(df):
    

    # Verificar se já existe uma seleção de continentes no session state
    if 'filtro_continente_grafico' not in st.session_state:
        st.session_state['filtro_continente_grafico'] = continentes  # Selecionar todos os continentes inicialmente

    # Multiselect para selecionar continentes no gráfico
    continentes_selecionados = st.multiselect(
        "Selecione os continentes para o gráfico",
        options=continentes,
        default=st.session_state['filtro_continente_grafico']
    )

    # Atualizar o session state com a seleção atual para o gráfico
    st.session_state['filtro_continente_grafico'] = continentes_selecionados

    # Filtrar os dados para apenas os continentes selecionados
    df_continentes = df[df['Países'].isin(st.session_state['filtro_continente_grafico'])]
    
    # Somar as visitas por continente ao longo dos meses
    df_continentes_soma = df_continentes.groupby('Países').sum()

    # Remover a coluna 'Total_Visitas' do DataFrame (caso já tenha sido adicionada)
    if 'Total_Visitas' in df_continentes_soma.columns:
        df_continentes_soma = df_continentes_soma.drop(columns=['Total_Visitas'])

    # Plotar o gráfico de linha
    st.subheader("Visitas por Continente ao Longo dos Meses")
    fig, ax = plt.subplots()
    df_continentes_soma.T.plot(ax=ax)  # Transpor os dados para exibir cada continente como uma linha
    plt.ylabel("Número de Visitas")
    plt.xlabel("Meses")
    st.pyplot(fig)


def exibir_tabela_interativa():
    st.subheader("Tabela Interativa de Dados")


    # Carregar e tratar os dados usando a função que você forneceu
    df = carregar_e_tratar_dados()

    # Se a tabela estiver vazia, mostrar uma mensagem de erro
    if df.empty:
        st.error("Nenhum dado disponível para exibir.")
        return

    # Multiselect para o usuário escolher quais colunas exibir
    colunas_selecionadas = st.multiselect(
        "Escolha as colunas que deseja visualizar", 
        options=df.columns.tolist(),  # Lista de todas as colunas
        default=df.columns.tolist()  # Selecionar todas as colunas por padrão
    )

    # Filtrar o DataFrame para mostrar apenas as colunas selecionadas
    df_filtrado = df[colunas_selecionadas]

    # Exibir a tabela filtrada e interativa
    st.dataframe(df_filtrado)

    # Botão para baixar os dados filtrados
    st.download_button(
        label="Baixar tabela filtrada em CSV",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

def exibir_histograma(df):
    st.subheader("Histograma de Visitas por Países")
    
    # Selecionar uma coluna para o histograma (uma coluna de meses, por exemplo)
    coluna = st.selectbox("Escolha a coluna para o histograma", df.columns[1:])
    
    # Plotar o histograma
    fig, ax = plt.subplots()
    sns.histplot(df[coluna], kde=True, ax=ax)  # Histograma com densidade de Kernel (KDE)
    ax.set_xlabel("Número de Visitas")
    ax.set_ylabel("Frequência")
    sns.histplot(df[coluna], kde=True, bins=30, ax=ax)  # Ajuste o número de bins conforme necessário

    
    # Exibir o gráfico
    st.pyplot(fig)

    # Média geral das entradas por mês
    media_mes = df[coluna].mean()
    st.metric(f"Média de {coluna}", round(media_mes))

    # Somar total de entradas por mês (se houver colunas mensais como janeiro, fevereiro etc.)
    soma_mes = df[coluna].sum()
    st.metric(f"Soma de {coluna}", round(soma_mes))

# Função para exibir o scatter plot (dispersão)
def exibir_scatter_plot(df):
    st.subheader("Gráfico de Dispersão (Scatter Plot)")
    
    # Selecionar duas colunas para o gráfico de dispersão
    coluna_x = st.selectbox("Escolha a coluna para o eixo X", df.columns[1:])
    coluna_y = st.selectbox("Escolha a coluna para o eixo Y", df.columns[1:], index=1)  # Para o eixo Y, escolha uma diferente de X
    
    # Plotar o scatter plot
    fig, ax = plt.subplots()
    ax.scatter(df[coluna_x], df[coluna_y])
    ax.set_xlabel(f"{coluna_x} (Eixo X)")
    ax.set_ylabel(f"{coluna_y} (Eixo Y)")
    ax.set_title(f"Dispersão entre {coluna_x} e {coluna_y}")
    
    # Exibir o gráfico
    st.pyplot(fig)

