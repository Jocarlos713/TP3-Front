import streamlit as st
from ui import pagina_dashboard, pagina_upload
from ui import aplicar_color_picker

def main():
    # Sidebar para navegação entre as páginas

    aba = st.sidebar.radio("Navegue pelas páginas", ["Upload de Arquivo CSV", "Dashboard de Turismo"])

    # Aplicar o color picker na página do dashboard
    if aba == "Upload de Arquivo CSV":
        pagina_upload()  # Página para upload do arquivo CSV
        
    elif aba == "Dashboard de Turismo":
        
        pagina_dashboard()  # Página do dashboard de turismo
        aplicar_color_picker()


if __name__ == '__main__':
    main()

    
