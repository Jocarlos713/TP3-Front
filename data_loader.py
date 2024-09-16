import pandas as pd
import streamlit as st
import pandas as pd

# Função para carregar e tratar o arquivo CSV para o dashboard (tratamento específico)
@st.cache_data  # Utilizando a funcionalidade de cache
def carregar_e_tratar_dados():
    df = pd.read_excel('2675.xls', sheet_name= '2019', skiprows=5).iloc[:102]
    df = df.drop([0, 1])
    df = df.drop(columns=['Total'])
    df = df.rename(columns={"Unnamed: 0": 'Países'})
  
    # Converter colunas numéricas (todas as colunas exceto a primeira)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
