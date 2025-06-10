import streamlit as st

def exibir_reagentes():
    df = st.session_state.dados

    reag_df = df[df["categoria"] == "Reagente"]

    st.title("🧬 Protocolos de Reagentes")
    st.markdown("Esta seção mostra os protocolos usados como reagentes em outros procedimentos.")

    if reag_df.empty:
        st.info("Nenhum protocolo de reagente cadastrado ainda.")
        return

    for _, row in reag_df.iterrows():
        nome = row["nome"]
        autor = row["autor"]
        data = row["data"]
        conteudo = row["conteudo"]
        versao = row["versao"]

        with st.expander(f"{nome} (versão {versao})"):
            st.markdown(f"**Criado por:** {autor}  \n**Data:** {data}")
            st.markdown(f"**Conteúdo:**  \n{conteudo}")
