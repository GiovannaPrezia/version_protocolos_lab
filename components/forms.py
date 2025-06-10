import streamlit as st
import datetime
import uuid
import pandas as pd

def exibir_formulario():
    with st.form("form_protocolo"):
        st.subheader("Cadastro de novo protocolo")

        nome = st.text_input("Nome do protocolo")
        grupo = st.selectbox("Grupo responsável", ["GRUPO CARDIO", "GRUPO TRONCO", "GRUPO SEILA", "GRUPO MARCO", "OUTRO"])
        categoria = st.selectbox("Categoria", ["PCR", "Cultura Celular", "Extração", "Imunofluorescência", "Outro"])
        validade = st.date_input("Validade", value=datetime.date.today())

        autor = st.text_input("Seu nome")
        email = st.text_input("Seu e-mail")
        departamento = st.text_input("Departamento")
        cargo = st.text_input("Cargo")
        conteudo = st.text_area("Conteúdo do protocolo", height=200)

        enviar = st.form_submit_button("Salvar")

        if enviar:
            if not nome or not autor or not conteudo:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
                return

            df = st.session_state.dados
            hoje = datetime.date.today().isoformat()
            ja_existe = df[df["nome"] == nome]
            versao = ja_existe["versao"].max() + 1 if not ja_existe.empty else 1
            historico = f"[{hoje}] {autor} criou a versão {versao}"

            novo = {
                "id": str(uuid.uuid4())[:8],
                "nome": nome,
                "grupo": grupo,
                "categoria": categoria,
                "versao": versao,
                "data": hoje,
                "validade": validade.isoformat(),
                "autor": autor,
                "email": email,
                "departamento": departamento,
                "cargo": cargo,
                "conteudo": conteudo,
                "arquivo_nome": "",  # reservado para futuras melhorias
                "historico": historico
            }

            st.session_state.dados = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            st.success(f"✅ Protocolo '{nome}' salvo como versão {versao}.")
