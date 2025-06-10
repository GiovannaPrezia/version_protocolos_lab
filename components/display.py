import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado.")
        return

    st.title("📚 Controle de Versionamento de Protocolos")

    for grupo in df["grupo"].unique():
        st.markdown(f"### 🧪 {grupo}")
        grupo_df = df[df["grupo"] == grupo]
        for categoria in grupo_df["categoria"].unique():
            st.markdown(f"#### 📂 {categoria}")
            cat_df = grupo_df[grupo_df["categoria"] == categoria]
            for _, row in cat_df.iterrows():
                with st.expander(f"📄 {row['nome']} (versão {row['versao']})"):
                    st.markdown(f"**Autor:** {row['autor']} ({row['email']})")
                    st.markdown(f"**Departamento:** {row['departamento']} | **Cargo:** {row['cargo']}")
                    st.markdown(f"**Data de criação:** {row['data']}  \n**Validade:** {row['validade']}")
                    st.markdown(f"**Categoria:** {row['categoria']}")
                    st.markdown(f"**Grupo:** {row['grupo']}")
                    st.markdown(f"🕓 Histórico: _{row['historico']}_")
                    st.markdown("**Conteúdo:**")
                    st.code(row["conteudo"], language="text")
