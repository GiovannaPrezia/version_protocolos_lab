import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado.")
        return

    grupos = sorted(df["grupo"].dropna().unique())
    grupo_filtro = st.sidebar.selectbox("Filtrar por grupo", ["Todos"] + grupos)

    if grupo_filtro != "Todos":
        df = df[df["grupo"] == grupo_filtro]

    st.title("📚 Controle de Versionamento de Protocolos")

    for grupo in df["grupo"].unique():
        st.markdown(f"## 🧪 {grupo}")
        grupo_df = df[df["grupo"] == grupo]
        for categoria in grupo_df["categoria"].unique():
            st.markdown(f"### 📂 {categoria}")
            cat_df = grupo_df[grupo_df["categoria"] == categoria]
            for _, row in cat_df.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    if isinstance(row["arquivo_nome"], str) and row["arquivo_nome"].endswith((".png", ".jpg", ".jpeg")):
                        st.image(row["arquivo_nome"], width=100)
                    else:
                        st.markdown("📄")
                with col2:
                    st.markdown(f"**{row['nome']}** (versão {row['versao']})  \n**Autor:** {row['autor']}  \n**Validade:** {row['validade']}")
                    st.markdown(f"🕓 *{row['historico']}*")
