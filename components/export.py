import streamlit as st

def exibir_exportacoes():
    df = st.session_state.dados

    if df.empty:
        st.warning("Nenhum protocolo disponível para exportação.")
        return

    st.download_button(
        label="📥 Baixar todos os dados (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="backup_protocolos.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("🔄 Restaurar backup")
    arquivo = st.file_uploader("Enviar backup CSV", type=["csv"])
    if arquivo:
        import pandas as pd
        try:
            novo_df = pd.read_csv(arquivo)
            st.session_state.dados = novo_df
            st.success("Backup restaurado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao carregar o backup: {e}")
