import streamlit as st
from urllib.parse import unquote

def exibir_reagentes():
    df = st.session_state.dados
    reag_df = df[df["categoria"] == "🧪 Protocolo de Reagentes/Soluções"]

    st.title("🧬 Lista de Reagentes")
    st.markdown("Esta seção lista os protocolos classificados como reagentes/soluções.")

    if reag_df.empty:
        st.info("Nenhum reagente cadastrado ainda.")
        return

    query = st.query_params
    reagente_destaque = query.get("reagente", [None])[0]
    reagente_destaque = unquote(reagente_destaque) if reagente_destaque else None

    termo = st.text_input("🔍 Buscar reagente por nome")
    if termo:
        reag_df = reag_df[reag_df["nome"].str.contains(termo, case=False, na=False)]

    for _, row in reag_df.iterrows():
        aberto = row["nome"].lower() == reagente_destaque.lower() if reagente_destaque else False
        with st.container():
            st.markdown(f"<h5>📘 {row['nome']} (versão {row['versao']})</h5>", unsafe_allow_html=True)
            if aberto or st.button(f"🔍 Ver {row['nome']}", key=row['id']):
                st.markdown(f"<h6 style='color:#ffd700;'>📂 {row['categoria']}</h6>", unsafe_allow_html=True)
                st.markdown(f"👤 **Autor:** {row['autor']} ({row['email']})")
                st.markdown(f"🏢 **Departamento:** {row['departamento']} • **Cargo:** {row['cargo']}")
                st.markdown(f"📅 **Data:** {row['data']} • **Validade:** {row['validade']}")
                st.markdown("📄 **Conteúdo do reagente:**")
                st.code(row["conteudo"], language="text")
                st.markdown("🕘 **Histórico:**")
                st.code(row["historico"], language="text")
                if st.button(f"🗑️ Excluir (ID: {row['id']})", key=f"del_{row['id']}"):
                    st.session_state.dados = st.session_state.dados[st.session_state.dados["id"] != row["id"]]
                    st.success("Protocolo removido com sucesso!")
                    st.experimental_rerun()
