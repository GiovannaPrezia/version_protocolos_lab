import streamlit as st
from urllib.parse import quote
from datetime import datetime

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

    st.markdown("## Protocolos cadastrados")
    termo = st.text_input("🔎 Filtrar protocolos")

    if termo:
        df = df[df["nome"].str.contains(termo, case=False, na=False)]

    col_main, col_side = st.columns([4, 1.7])

    with col_main:
        for grupo in df["grupo"].dropna().unique():
            st.markdown(f"### 🧪 {grupo}")
            grupo_df = df[df["grupo"] == grupo]

            for categoria in grupo_df["categoria"].dropna().unique():
                st.markdown(f"#### 📂 {categoria}")
                cat_df = grupo_df[grupo_df["categoria"] == categoria]

                cols = st.columns(3)
                for idx, (_, row) in enumerate(cat_df.iterrows()):
                    with cols[idx % 3]:
                        st.markdown(
                            f"""
                            <div style='border:1px solid #555; border-radius:10px; padding:10px; background-color:#111; color:#eee; margin-bottom:15px;'>
                                <div style='font-size:12px; color:#aaa;'>📄 {row['nome']}</div>
                                <div style='font-size:11px; color:#888;'>Versão {row['versao']} • {row['data']}</div>
                                <div style='margin-top:10px;'>
                                    <a href='#{quote(row["nome"])}' style='color:#4da6ff; font-size:12px;'>🔍 Ver detalhes</a>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        ) 

    with col_side:
        st.markdown("### 🕒 Atividades recentes")
        recentes = df.sort_values("data", ascending=False).head(6)

        for _, row in recentes.iterrows():
            st.markdown(
                f"""
                <div style='border-left: 3px solid #4da6ff; padding-left: 10px; margin-bottom: 15px;'>
                    <div style='font-size:13px;'><b>{row['autor']}</b></div>
                    <div style='font-size:12px;'>📄 <a href='#{quote(row["nome"])}' style='color:#4da6ff;'>{row['nome']}</a></div>
                    <div style='font-size:11px; color:#999;'>{row['data']} | ID: {row['id']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
