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

    st.title("📚 LabTrack: Plataforma de Controle de Versionamento de Protocolos")
    st.markdown("### Protocolos cadastrados")

    col_main, col_atividades = st.columns([4, 1.5])

    with col_main:
        for grupo in df["grupo"].unique():
            st.markdown(f"### 🧪 {grupo}")
            grupo_df = df[df["grupo"] == grupo]
            for categoria in grupo_df["categoria"].unique():
                st.markdown(f"#### 📂 {categoria}")
                cat_df = grupo_df[grupo_df["categoria"] == categoria]

                cards = []
                for _, row in cat_df.iterrows():
                    nome = row["nome"][:28] + "..." if len(row["nome"]) > 28 else row["nome"]
                    data = row["data"]
                    versao = row["versao"]

                    card_html = f"""
                        <div style="
                            border: 1px solid #444; 
                            padding: 12px; 
                            border-radius: 10px; 
                            background-color: #1e1e1e;
                            text-align: center;
                            height: 150px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                            overflow: hidden;
                        ">
                            <div style="font-size: 20px; margin-bottom: 10px;">📄</div>
                            <div style="font-size: 14px; color: #bbb;">{nome}</div>
                            <div style="font-size: 12px; color: #888;">{data}</div>
                            <div style="font-size: 11px; color: #888;">Versão {versao}</div>
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
