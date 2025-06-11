import streamlit as st

def exibir_reagentes():
    df = st.session_state.dados
    reag_df = df[df["categoria"] == "🧪 Protocolo de Reagentes/Soluções"]

    st.title("🧬 Protocolos de Reagentes")
    st.markdown("Esta seção lista os protocolos classificados como reagentes/soluções.")

    if reag_df.empty:
        st.info("Nenhum reagente cadastrado ainda.")
        return

    for _, row in reag_df.iterrows():
        with st.expander(f"{row['nome']} (versão {row['versao']})"):
            st.markdown(f"**Autor:** {row['autor']}  \n**Validade:** {row['validade']}")
            st.markdown("**Conteúdo do reagente:**")
            st.code(row["conteudo"], language="text")
