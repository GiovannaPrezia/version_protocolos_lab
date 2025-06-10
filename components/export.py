import streamlit as st
import pandas as pd
import io

def exibir_exportacoes():
    st.subheader("📤 Exportar / Backup de Protocolos")

    df = st.session_state.dados

    if df.empty:
        st.warning("Nenhum dado disponível para exportação.")
    else:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar todos os protocolos (CSV)",
            data=csv,
            file_name="protocolos_backup.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.subheader("📁 Restaurar protocolos a partir de backup")

    arquivo = st.file_uploader("Selecione um arquivo CSV com os dados salvos")

    if arquivo:
        try:
            novo_df = pd.read_csv(arquivo)
            st.session_state.dados = pd.concat([st.session_state.dados, novo_df], ignore_index=True).drop_duplicates(subset=["id"])
            st.success("Backup restaurado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao carregar backup: {e}")
