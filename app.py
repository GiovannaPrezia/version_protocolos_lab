import streamlit as st
import pandas as pd
from components import forms, display, export, reagentes

st.set_page_config(page_title="Controle de Protocolos", page_icon="🧪", layout="wide")

# Inicializar DataFrame no session_state
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "id", "nome", "grupo", "categoria", "versao", "data", "validade",
        "autor", "email", "departamento", "cargo", "conteudo",
        "reagentes", "arquivo_nome", "arquivo_bytes", "historico"
    ])

# Menu lateral com navegação
menu = st.sidebar.radio("Menu", [
    "➕ Novo Protocolo",
    "📄 Visualizar Protocolos",
    "🧬 Protocolos de Reagentes",
    "📤 Exportar / Backup"
])

# Direcionamento das páginas
if menu == "➕ Novo Protocolo":
    forms.exibir_formulario()

elif menu == "📄 Visualizar Protocolos":
    display.exibir_protocolos()

elif menu == "🧬 Protocolos de Reagentes":
    reagentes.exibir_reagentes()

elif menu == "📤 Exportar / Backup":
    export.exibir_exportacoes()
