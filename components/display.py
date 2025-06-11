import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado ainda.")
        return

    # Ocultar protocolos de reagentes
    df = df[df["categoria"] != "🧪 Protocolo de Reagentes/Soluções"]

    # Título fixo
    st.markdown("""
        <h1 style='text-align: center; color: #fff; margin-bottom: 10px;'>
            🔬 LabTrack: Plataforma de Controle de Versionamento de Protocolos Laboratoriais
        </h1>
        <hr style='border: 1px solid #555; margin-top: -10px;'>
    """, unsafe_allow_html=True)

    st.title("📄 Protocolos Gerais")
    st.subheader("Visualize os protocolos laboratoriais cadastrados")

    col_main, col_atividades = st.columns([4, 1.6])

    with col_main:
        grupos = df["grupo"].dropna().unique()
        for grupo in grupos:
            st.markdown(f"### 🧪 {grupo}")
            grupo_df = df[df["grupo"] == grupo]

            for categoria in grupo_df["categoria"].unique():
                st.markdown(f"#### 📂 {categoria}")
                cat_df = grupo_df[grupo_df["categoria"] == categoria]

                for _, row in cat_df.iterrows():
                    nome = row["nome"]
                    versao = row["versao"]
                    data = row["data"]
                    autor = row["autor"]
                    validade = row["validade"]
                    conteudo = row["conteudo"]
                    reagentes = row.get("reagentes", [])
                    anexo_nome = row.get("arquivo_nome", "")
                    anexo_bytes = row.get("arquivo_bytes", None)

                    with st.expander(f"{nome} (Versão {versao} • {data})"):
                        st.markdown(f"**Autor:** {autor}")
                        st.markdown(f"**Validade:** {validade}")
                        st.markdown("**Conteúdo:**")
                        st.code(conteudo, language="text")

                        if reagentes:
                            links = [
                                f'<a href="/?reagente={r}" style="color:#4da6ff;">{r}</a>'
                                for r in reagentes
                            ]
                            st.markdown(f"**Reagentes utilizados:** {' • '.join(links)}", unsafe_allow_html=True)

                        if anexo_bytes:
                            st.download_button(
                                label=f"📎 Baixar anexo: {anexo_nome}",
                                data=anexo_bytes,
                                file_name=anexo_nome
                            )

    # Painel lateral de atividades recentes
    with col_atividades:
        st.markdown("### 🕒 Atividades recentes")
        atividades = st.session_state.dados.sort_values("data", ascending=False).head(10)

        for _, row in atividades.iterrows():
            atividade_html = f"""
                <div style="border-left: 3px solid #2c6dfc; padding-left: 10px; margin-bottom: 20px;">
                    <div style="font-size: 13px; color: #fff;"><b>{row['autor']}</b></div>
                    <div style="font-size: 12px; color: #bbb;">🧾 {row['nome']}</div>
                    <div style="font-size: 11px; color: #888;">{row['data']} | ID: {row['id']}</div>
                </div>
            """
            st.markdown(atividade_html, unsafe_allow_html=True)
