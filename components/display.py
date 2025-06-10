import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado ainda.")
        return

    st.title("📚 Controle de Versionamento de Protocolos")
    st.subheader("Gerencie e visualize seus protocolos de forma eficiente")

    col_main, col_atividades = st.columns([4, 1.6])

    with col_main:
        grupos = df["grupo"].dropna().unique()
        for grupo in grupos:
            st.markdown(f"### 🧪 {grupo}")
            grupo_df = df[df["grupo"] == grupo]

            for categoria in grupo_df["categoria"].unique():
                st.markdown(f"#### 📂 {categoria}")
                cat_df = grupo_df[grupo_df["categoria"] == categoria]

                cards = []
                for _, row in cat_df.iterrows():
                    nome = row["nome"][:30] + "..." if len(row["nome"]) > 30 else row["nome"]
                    data = row["data"]
                    versao = row["versao"]
                    reagentes = row.get("reagentes", [])
                    tem_anexo = bool(row.get("arquivo_nome"))

                    reagentes_html = ""
                    if isinstance(reagentes, list) and reagentes:
                        for r in reagentes:
                            reagentes_html += f'<a href="#🧬 Protocolos de Reagentes" style="color:#4da6ff;">{r}</a>, '
                        reagentes_html = f"<div style='font-size:11px;color:#4da6ff;'>Reagentes: {reagentes_html[:-2]}</div>"

                    icone = "📎" if tem_anexo else "📄"

                    card_html = f"""
                        <div style="
                            border: 1px solid #444; 
                            padding: 12px; 
                            border-radius: 10px; 
                            background-color: #1e1e1e;
                            text-align: center;
                            height: 170px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                            overflow: hidden;
                            margin-bottom: 10px;
                        ">
                            <div style="font-size: 24px; margin-bottom: 8px;">{icone}</div>
                            <div style="font-size: 14px; color: #ccc;">{nome}</div>
                            <div style="font-size: 12px; color: #999;">Versão {versao} • {data}</div>
                            {reagentes_html}
                        </div>
                    """
                    cards.append(card_html)

                for i in range(0, len(cards), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(cards):
                            with cols[j]:
                                st.markdown(cards[i + j], unsafe_allow_html=True)

    with col_atividades:
        st.markdown("### 🕒 Atividades recentes")
        atividades = df.sort_values("data", ascending=False).head(10)

        for _, row in atividades.iterrows():
            atividade_html = f"""
                <div style="border-left: 3px solid #2c6dfc; padding-left: 10px; margin-bottom: 20px;">
                    <div style="font-size: 13px; color: #fff;"><b>{row['autor']}</b></div>
                    <div style="font-size: 12px; color: #bbb;">🧾 {row['nome']}</div>
                    <div style="font-size: 11px; color: #888;">{row['data']} | ID: {row['id']}</div>
                </div>
            """
            st.markdown(atividade_html, unsafe_allow_html=True)
