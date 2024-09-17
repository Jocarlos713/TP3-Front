import streamlit as st
import pandas as pd
import time
from data_loader import carregar_e_tratar_dados
from visualization import exibir_grafico_pizza, exibir_grafico_linha, exibir_grafico_linha_por_continente
from visualization import exibir_tabela_interativa
from visualization import exibir_histograma
from visualization import exibir_scatter_plot


# Função para exibir a página do dashboard
def pagina_dashboard():
    st.title("Chegada mensal de turistas pelo  Rio de Janeiro, segundo continentes e países de residência permanente - Via aérea  - 2019")

    # Carregar e tratar os dados para o dashboard
    df = carregar_e_tratar_dados()

    # Exibir o dataframe
    exibir_tabela_interativa()

    # Exibir o gráfico de pizza
    exibir_grafico_pizza(df)

    # Verificar se existe algo no session_state relacionado à seleção de país
    if 'pais_selecionado' not in st.session_state:
        st.session_state['pais_selecionado'] = df['Países'].unique()[0]  # Definir o primeiro país como padrão

    # Interface para selecionar um país
    st.subheader("Selecione um País para Visualizar as Visitas ao Longo dos Meses")
    paises_disponiveis = df['Países'].unique()

    # Selecionar país, com a persistência do último selecionado
    pais_selecionado = st.selectbox("Escolha o país", paises_disponiveis, index=paises_disponiveis.tolist().index(st.session_state['pais_selecionado']))

    # Atualizar o session_state com o país selecionado
    st.session_state['pais_selecionado'] = pais_selecionado

    # Exibir o gráfico de linha com o país selecionado
    exibir_grafico_linha(df, pais_selecionado)

    exibir_grafico_linha_por_continente(df)

    exibir_histograma(df)

    exibir_scatter_plot(df)

# Função para a página de upload (separado)
def pagina_upload():
    st.title("Upload de Arquivo CSV - Dados de Turismo do Data.Rio")

    uploaded_file = st.file_uploader("Faça o upload do arquivo CSV", type=["csv"])

    if uploaded_file:
        # Adicionando o spinner de carregamento
        with st.spinner('Carregando o arquivo...'):
            # Criar barra de progresso
            progress_bar = st.progress(0)

            # Simulando progresso do carregamento (ajuste para o tempo real de processamento)
            for perc in range(0, 101, 10):
                time.sleep(0.1)  # Simulando um tempo de processamento
                progress_bar.progress(perc)

            # Exibir mensagem de sucesso após o carregamento
            st.success("Arquivo CSV carregado com sucesso!")

            # Carregar o CSV e exibir
            df = pd.read_csv(uploaded_file)
            st.write(df)  # Exibindo o dataframe para verificar o conteúdo

# Função para aplicar cores personalizadas com Color Picker
def aplicar_color_picker():
    st.title("Personalização de Cores")

    # Color Picker para o fundo
    cor_fundo = st.color_picker("Escolha a cor de fundo", "#000000")  # Preto por padrão

    # Color Picker para o texto (fonte)
    cor_fonte = st.color_picker("Escolha a cor da fonte", "#FFFFFF")  # Branco por padrão

    # Aplicar as cores escolhidas para o fundo e o texto
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {cor_fundo};
                color: {cor_fonte};
            }}
            h1, h2, h3, h4, h5, h6, p, div, span {{
                color: {cor_fonte} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )