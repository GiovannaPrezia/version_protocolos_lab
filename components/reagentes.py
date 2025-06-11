import streamlit as st
from urllib.parse import unquote

def exibir_reagentes():
    df = st.session_state.dados
    reag_df = df[df["categoria"] == "🧪 Protocolo de Reagentes/Soluções"]

    st.markdown("""
        <h2 style='text-align: center; color: #fff; margin-bottom: 0;'>
            🔬 LabTrack: Plataforma de Controle de Versionamento de Protocolos Laboratoriais
        </h2>
        <hr style='border: 1px solid #555;'>
    """, unsafe_allow_html=True)

    st.title("🤔 Protocolos de Reagentes")
    st.markdown("Esta seção lista os protocolos classificados como reagentes/soluções.")

    if reag_df.empty:
        st.info("Nenhum reagente cadastrado ainda.")
        return

    query = st.query_params
    reagente_destaque = query.get("reagente", [None])[0]
    reagente_destaque = unquote(reagente_destaque) if reagente_destaque else None

    termo = st.text_input("🔍 Buscar reagente por nome")
    if termo:
        reag_df = reag_df[reag_df["nome"].str.contains(termo, case=False, na=False)]

    for _, row in reag_df.iterrows():
        nome = row["nome"]
        versao = row["versao"]
        autor = row["autor"]
        validade = row["validade"]
        conteudo = row["conteudo"]
        protocolo_id = row["id"]

        aberto = nome.lower() == reagente_destaque.lower() if reagente_destaque else False

        with st.expander(f"{nome} (versão {versao})", expanded=aberto):
            st.markdown(f"**Autor:** {autor}")
            st.markdown(f"**Validade:** {validade}")
            st.markdown("**Conteúdo do reagente:**")
            st.code(conteudo, language="text")

            if st.button(f"🗑️ Excluir este protocolo (ID: {protocolo_id})", key=protocolo_id):
                st.session_state.dados = st.session_state.dados[st.session_state.dados["id"] != protocolo_id]
                st.success(f"Protocolo '{nome}' removido com sucesso!")
                st.experimental_rerun()
