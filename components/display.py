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

    col_main, col_sidebar = st.columns([4, 1.5])  # corpo principal + painel lateral

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
                    card = f"""
                        <div style="border:1px solid #444;padding:12px;border-radius:8px;background:#1e1e1e;margin:5px;width:100%;text-align:center;">
                            <div style="font-size:14px;color:#bbb;">📝 {nome}</div>
                            <div style="font-size:12px;color:#999;margin-top:4px;">{row["data"]}</div>
                            <div style="font-size:32px;margin:6px 0;">📄</div>
                            <div style="font-size:11px;color:#888;">Versão {row["versao"]}</div>
                        </div>
                    """
                    cards.append(card)

                # exibe os cards 3 por linha
                for i in range(0, len(cards), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(cards):
                            with cols[j]:
                                st.markdown(cards[i + j], unsafe_allow_html=True)

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
