from components import forms, display, export
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Controle de Protocolos", page_icon="🧪")

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "id", "nome", "grupo", "categoria", "versao", "data", "validade",
        "autor", "email", "departamento", "cargo",
        "conteudo", "arquivo_nome", "historico"
    ])

menu = st.sidebar.radio("Menu", ["➕ Novo Protocolo", "📄 Visualizar Protocolos", "📤 Exportar/Backup"])

if menu == "➕ Novo Protocolo":
    forms.exibir_formulario()

elif menu == "📄 Visualizar Protocolos":
    display.exibir_protocolos()

elif menu == "📤 Exportar/Backup":
    export.exibir_exportacoes()
