import streamlit as st
from datetime import datetime
from urllib.parse import quote

def exibir_protocolos():
    df = st.session_state.dados
    if df.empty:
        st.info("Nenhum protocolo cadastrado ainda.")
        return

    df = df[df["categoria"] != "🧪 Protocolo de Reagentes/Soluções"]

    st.markdown("""
        <h2 style='text-align: center;'>🔬 LabTrack: Plataforma de Controle de Versionamento de Protocolos Laboratoriais</h2>
        <hr>
    """, unsafe_allow_html=True)

    st.subheader("📄 Protocolos Gerais")

    for grupo in df["grupo"].dropna().unique():
        st.markdown(f"### 🧪 {grupo}")
        grupo_df = df[df["grupo"] == grupo]

        for categoria in grupo_df["categoria"].unique():
            st.markdown(f"#### 📂 {categoria}")
            cat_df = grupo_df[grupo_df["categoria"] == categoria]

            for _, row in cat_df.iterrows():
                with st.container():
                    st.markdown(f"**{row['nome']}** (Versão {row['versao']})")
                    if st.button("📖 Ver detalhes", key=f"abrir_{row['id']}"):
                        st.markdown("---")
                        st.markdown(f"📂 **Categoria:** {row['categoria']}")
                        st.markdown(f"👤 **Autor:** {row['autor']} ({row['email']})")
                        st.markdown(f"🏢 **Departamento:** {row['departamento']} • **Cargo:** {row['cargo']}")
                        st.markdown(f"📅 **Data:** {row['data']} • **Validade:** {row['validade']}")
                        st.markdown(f"📝 **Conteúdo:**\n\n{row['conteudo']}")

                        # Exibir reagentes como links clicáveis
                        if row["reagentes"]:
                            links = [
                                f'<a href="/?reagente={quote(r)}" style="color:#4da6ff;">{r}</a>'
                                for r in row["reagentes"]
                            ]
                            st.markdown(f"🧬 **Reagentes:** {' • '.join(links)}", unsafe_allow_html=True)

                        # Histórico do protocolo
                        st.markdown("🕘 **Histórico:**")
                        st.code(row["historico"] or "Sem histórico disponível", language="text")

                        # Botão para download, se houver anexo
                        if row["arquivo_bytes"]:
                            st.download_button("📎 Baixar Anexo", row["arquivo_bytes"], file_name=row["arquivo_nome"])
