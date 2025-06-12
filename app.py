import streamlit as st
import pandas as pd
from components import forms, display, export, reagentes

st.set_page_config(page_title="Controle de Protocolos", page_icon="🧪", layout="wide")

# Inicializar DataFrame
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "id", "nome", "grupo", "categoria", "versao", "data", "validade",
        "autor", "email", "departamento", "cargo", "conteudo",
        "reagentes", "arquivo_nome", "arquivo_bytes", "historico"
    ])

menu = st.sidebar.radio("Menu", [
    "➕ Cadastrar Novo Protocolo",
    "📄 Protocolos Gerais",
    "🧬 Lista de Reagentes",
    "📤 Exportar / Backup"
])

if menu == "➕ Cadastrar Novo Protocolo":
    forms.exibir_formulario()
elif menu == "📄 Protocolos Gerais":
    display.exibir_protocolos()
elif menu == "🧬 Lista de Reagentes":
    reagentes.exibir_reagentes()
elif menu == "📤 Exportar / Backup":
    export.exibir_exportacoes()
