# app.py
import streamlit as st
import pandas as pd
import datetime
import uuid
import io

st.set_page_config(page_title="Controle de Protocolos", page_icon="🧪")

# ---------- Inicialização ----------
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["id", "nome", "versao", "data", "autor", "conteudo"])

# ---------- Título e Navegação ----------
st.title("📚 Controle de Protocolos de Laboratório")

aba = st.sidebar.radio("Navegação", ["📄 Visualizar", "➕ Novo Protocolo", "📤 Exportar CSV"])

# ---------- Função para filtrar ----------
def filtrar_protocolos(df, nome=None, autor=None):
    if nome:
        df = df[df["nome"].str.contains(nome, case=False, na=False)]
    if autor:
        df = df[df["autor"].str.contains(autor, case=False, na=False)]
    return df

# ---------- Aba: Visualizar ----------
if aba == "📄 Visualizar":
    st.subheader("Protocolos cadastrados")

    with st.expander("🔍 Filtrar protocolos"):
        filtro_nome = st.text_input("Filtrar por nome:")
        filtro_autor = st.text_input("Filtrar por autor:")
        df_filtrado = filtrar_protocolos(st.session_state.dados, filtro_nome, filtro_autor)
    else:
        df_filtrado = st.session_state.dados

    if df_filtrado.empty:
        st.info("Nenhum protocolo encontrado.")
    else:
        for nome, grupo in df_filtrado.groupby("nome"):
            grupo = grupo.sort_values("versao", ascending=False)
            ultima = grupo.iloc[0]
            with st.expander(f"🧪 {nome} (versão {ultima['versao']})"):
                st.markdown(f"**Autor:** {ultima['autor']} | **Data:** {ultima['data']}")
                st.code(ultima["conteudo"], language="text")

# ---------- Aba: Novo Protocolo ----------
elif aba == "➕ Novo Protocolo":
    st.subheader("Adicionar novo protocolo")

    with st.form("novo_protocolo"):
        nome = st.text_input("Nome do protocolo")
        autor = st.text_input("Seu nome")
        conteudo = st.text_area("Conteúdo do protocolo", height=200)
        enviar = st.form_submit_button("Salvar")

        if enviar and nome and autor and conteudo:
            df = st.session_state.dados
            hoje = datetime.date.today().isoformat()
            ja_existe = df[df["nome"] == nome]
            versao = ja_existe["versao"].max() + 1 if not ja_existe.empty else 1
            novo = {
                "id": str(uuid.uuid4())[:8],
                "nome": nome,
                "versao": versao,
                "data": hoje,
                "autor": autor,
                "conteudo": conteudo
            }
            st.session_state.dados = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            st.success(f"✅ Protocolo '{nome}' salvo como versão {versao}.")

# ---------- Aba: Exportar CSV ----------
elif aba == "📤 Exportar CSV":
    st.subheader("Exportar protocolos")

    df_exportar = st.session_state.dados
    if df_exportar.empty:
        st.warning("Nenhum dado para exportar.")
    else:
        csv = df_exportar.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name="protocolos_exportados.csv",
            mime="text/csv"
        )
