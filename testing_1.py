import streamlit as st
import pandas as pd
import datetime
import uuid

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

    if df_filtrado.empty:
        st.info("Nenhum protocolo encontrado.")
    else:
        for nome, grupo in df_filtrado.groupby("nome"):
            grupo = grupo.sort_values("versao", ascending=False)
            st.markdown(f"### 🧪 {nome}")
            for _, row in grupo.iterrows():
                with st.expander(f"📄 Versão {row['versao']}"):
                    st.markdown(f"**Autor:** {row['autor']}  \n**Data:** {row['data']}  \n**ID:** `{row['id']}`")
                    st.code(row["conteudo"], language="text")
                    if st.button(f"🗑️ Excluir esta versão", key=f"excluir_{row['id']}"):
                        st.session_state.dados = st.session_state.dados[st.session_state.dados["id"] != row["id"]]
                        st.success(f"Versão {row['versao']} do protocolo '{row['nome']}' excluída.")
                        st.experimental_rerun()

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
        nomes = sorted(df_exportar["nome"].unique())
        opcoes = ["Todos"] + nomes
        escolha = st.selectbox("Escolha um protocolo para exportar:", options=opcoes)

        if escolha == "Todos":
            df_escolhido = df_exportar
        else:
            df_escolhido = df_exportar[df_exportar["nome"] == escolha]

        csv = df_escolhido.to_csv(index=False).encode("utf-8")
        nome_arquivo = "todos_protocolos.csv" if escolha == "Todos" else f"{escolha.replace(' ', '_')}.csv"

        st.download_button(
            label=f"📥 Baixar CSV de '{escolha}'",
            data=csv,
            file_name=nome_arquivo,
            mime="text/csv"
        )
