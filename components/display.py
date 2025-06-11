import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado ainda.")
        return

    # Ocultar protocolos de reagentes
    df = df[df["categoria"] != "🧪 Protocolo de Reagentes/Soluções"]

    # Título da plataforma
    st.markdown("""
        <h2 style='text-align: center; color: #fff; margin-bottom: 0;'>
            🔬 LabTrack: Plataforma de Controle de Versionamento de Protocolos Laboratoriais
        </h2>
        <hr style='border: 1px solid #555;'>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 0;'>📄 Protocolos Gerais</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px;'>Visualize os protocolos laboratoriais cadastrados</p>", unsafe_allow_html=True)

    col_main, col_atividades = st.columns([4, 1.6])
 
    with col_main:
        grupos = df["grupo"].dropna().unique()
        for grupo in grupos:
            st.markdown(f"<h4 style='color:#fff;'>{grupo}</h4>", unsafe_allow_html=True)
            grupo_df = df[df["grupo"] == grupo]

            for categoria in grupo_df["categoria"].unique():
                st.markdown(f"<h5 style='color:#ffd700;'>📁 {categoria}</h5>", unsafe_allow_html=True)
                cat_df = grupo_df[grupo_df["categoria"] == categoria]

                for _, row in cat_df.iterrows():
                    protocolo_id = row["id"]
                    nome = row["nome"]
                    versao = row["versao"]
                    data = row["data"]
                    key = f"expand_{protocolo_id}"

                    # Criar sessão controlada por clique
                    if st.button(f"{nome} (Versão {versao} • {data})", key=key):
                        st.session_state["protocolo_aberto"] = protocolo_id

                    if st.session_state.get("protocolo_aberto") == protocolo_id:
                        autor = row["autor"]
                        validade = row["validade"]
                        conteudo = row["conteudo"]
                        reagentes = row.get("reagentes", [])
                        anexo_nome = row.get("arquivo_nome", "")
                        anexo_bytes = row.get("arquivo_bytes", None)

                        with st.container():
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

    with col_atividades:
        st.markdown("<h4 style='margin-bottom:10px;'>⏰ Atividades recentes</h4>", unsafe_allow_html=True)
        atividades = st.session_state.dados.sort_values("data", ascending=False).head(10)

        for _, row in atividades.iterrows():
            atividade_html = f"""
                <div style="border-left: 3px solid #2c6dfc; padding-left: 10px; margin-bottom: 20px;">
                    <div style="font-size: 13px; color: #fff;"><b>{row['autor']}</b></div>
                    <div style="font-size: 12px; color: #bbb;">🗒️ {row['nome']}</div>
                    <div style="font-size: 11px; color: #888;">{row['data']} | ID: {row['id']}</div>
                </div>
            """
            st.markdown(atividade_html, unsafe_allow_html=True)
