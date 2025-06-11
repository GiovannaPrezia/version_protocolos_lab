import streamlit as st

def exibir_reagentes():
    df = st.session_state.dados

    # Filtra apenas reagentes
    reag_df = df[df["categoria"] == "🧪 Protocolo de Reagentes/Soluções"]

    st.title("🧬 Protocolos de Reagentes")
    st.markdown("Esta seção lista os protocolos classificados como reagentes/soluções.")

    if reag_df.empty:
        st.info("Nenhum reagente cadastrado ainda.")
        return

    # Campo de busca
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

        with st.expander(f"{nome} (versão {versao})"):
            st.markdown(f"**Autor:** {autor}")
            st.markdown(f"**Validade:** {validade}")
            st.markdown("**Conteúdo do reagente:**")
            st.code(conteudo, language="text")

            # Botão de exclusão
            if st.button(f"🗑️ Excluir este protocolo (ID: {protocolo_id})", key=protocolo_id):
                st.session_state.dados = st.session_state.dados[st.session_state.dados["id"] != protocolo_id]
                st.success(f"Protocolo '{nome}' removido com sucesso!")
                st.experimental_rerun()
