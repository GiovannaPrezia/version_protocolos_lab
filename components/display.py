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
    st.markdown("### Protocolos cadastrados")

    col_main, col_sidebar = st.columns([4, 1.5])

    with col_main:
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

                        if st.button(f"🗑️ Excluir versão {row['versao']} do protocolo", key=row["id"]):
                            st.session_state.dados = st.session_state.dados[st.session_state.dados["id"] != row["id"]]
                            st.success(f"Versão {row['versao']} excluída com sucesso.")
                            st.experimental_rerun()

    with col_sidebar:
        st.markdown("### 🕒 Atividades recentes")
        atividades = []
        for _, row in df.sort_values("data", ascending=False).iterrows():
            atividades.append(f"""
                <div style="font-size:12px;margin-bottom:15px;">
                    <b>{row['autor']}</b><br>
                    🧾 <i>{row['nome']}</i><br>
                    🕓 {row['data']}<br>
                    <span style='font-size:11px;color:#888;'>ID: {row['id']}</span>
                </div>
            """)

        for evento in atividades[:10]:
            st.markdown(evento, unsafe_allow_html=True)
