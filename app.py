import streamlit as st
import pandas as pd
import datetime
import uuid

st.set_page_config(page_title="Controle de Protocolos", page_icon="🧪")

# Simulação de banco de dados
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["id", "nome", "versao", "data", "autor", "conteudo"])

st.title("📚 Versionamento de Protocolos de Laboratório")

aba = st.sidebar.radio("Navegação", ["📄 Visualizar", "➕ Novo Protocolo"])

df = st.session_state.dados

if aba == "📄 Visualizar":
    if df.empty:
        st.info("Nenhum protocolo cadastrado ainda.")
    else:
        for nome, grupo in df.groupby("nome"):
            grupo = grupo.sort_values("versao", ascending=False)
            ultima = grupo.iloc[0]
            with st.expander(f"{nome} - versão {ultima['versao']}"):
                st.markdown(f"**Autor:** {ultima['autor']} | **Data:** {ultima['data']}")
                st.code(ultima["conteudo"])
elif aba == "➕ Novo Protocolo":
    with st.form("novo_protocolo"):
        nome = st.text_input("Nome do protocolo")
        autor = st.text_input("Seu nome")
        conteudo = st.text_area("Conteúdo do protocolo", height=200)
        enviar = st.form_submit_button("Salvar")

        if enviar and nome and autor and conteudo:
            hoje = datetime.date.today().isoformat()
            existente = df[df["nome"] == nome]
            versao = existente["versao"].max() + 1 if not existente.empty else 1
            novo = {
                "id": str(uuid.uuid4())[:8],
                "nome": nome,
                "versao": versao,
                "data": hoje,
                "autor": autor,
                "conteudo": conteudo
            }
            st.session_state.dados = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            st.success(f"Protocolo '{nome}' salvo como versão {versao}.")
