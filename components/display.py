import streamlit as st
from datetime import datetime

def exibir_protocolos():
    df = st.session_state.dados

    if df.empty:
        st.info("Nenhum protocolo cadastrado.")
        return

    filtro = st.selectbox("Filtrar por categoria:", ["Todos"] + sorted(df["categoria"].unique()))
    if filtro != "Todos":
        df = df[df["categoria"] == filtro]

    for nome, grupo in df.groupby("nome"):
        grupo = grupo.sort_values("versao", ascending=False)
        st.markdown(f"## 🧪 {nome}")
        for _, row in grupo.iterrows():
            with st.expander(f"📄 Versão {row['versao']}"):
                st.markdown(f"**Autor:** {row['autor']} ({row['email']})")
                st.markdown(f"**Departamento:** {row['departamento']} | **Cargo:** {row['cargo']}")
                st.markdown(f"**Data:** {row['data']} | **Validade:** {row['validade']}")

                if datetime.fromisoformat(row["validade"]) < datetime.today():
                    st.error("⚠️ Protocolo vencido!")
                elif (datetime.fromisoformat(row["validade"]) - datetime.today()).days <= 7:
                    st.warning("⚠️ Protocolo próximo da validade")

                st.markdown(f"**Categoria:** {row['categoria']}")
                st.code(row["conteudo"], language="text")
                if row["pdf_nome"]:
                    st.markdown(f"📎 PDF anexado: `{row['pdf_nome']}`")
                st.markdown(f"🕓 Histórico: {row['historico']}")
