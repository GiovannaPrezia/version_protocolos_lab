import streamlit as st
import datetime
import uuid
import pandas as pd

def exibir_formulario():
    with st.form("form_protocolo"):
        st.subheader("Cadastro de novo protocolo")
        nome = st.text_input("Nome do protocolo")
        categoria = st.selectbox("Categoria", ["PCR", "Cultura Celular", "Extração", "Imunofluorescência", "Outro"])
        validade = st.date_input("Validade", value=datetime.date.today())
        autor = st.text_input("Seu nome")
        email = st.text_input("Seu e-mail")
        departamento = st.text_input("Departamento")
        cargo = st.text_input("Cargo")
        conteudo = st.text_area("Conteúdo do protocolo", height=200)
        pdf = st.file_uploader("Anexar PDF (opcional)", type=["pdf"])

        enviar = st.form_submit_button("Salvar")

        if enviar and nome and autor and conteudo:
            df = st.session_state.dados
            hoje = datetime.date.today().isoformat()
            ja_existe = df[df["nome"] == nome]
            versao = ja_existe["versao"].max() + 1 if not ja_existe.empty else 1
            pdf_nome = pdf.name if pdf else ""
            historico = f"[{hoje}] {autor} criou a versão {versao}"

            novo = {
                "id": str(uuid.uuid4())[:8],
                "nome": nome,
                "versao": versao,
                "data": hoje,
                "validade": validade.isoformat(),
                "categoria": categoria,
                "autor": autor,
                "email": email,
                "departamento": departamento,
                "cargo": cargo,
                "conteudo": conteudo,
                "pdf_nome": pdf_nome,
                "historico": historico
            }

            st.session_state.dados = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            st.success(f"✅ Protocolo '{nome}' salvo como versão {versao}.")
