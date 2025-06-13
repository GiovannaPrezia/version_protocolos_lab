import streamlit as st
from streamlit_quill import st_quill
from datetime import datetime
import uuid
import pandas as pd

def exibir_formulario():
    st.header("📋 Cadastrar Novo Protocolo")

    st.markdown("""
        <style>
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

    aba_protocolo, aba_reagente = st.tabs([
        "📑 CADASTRO DE PROTOCOLO",
        "🧪 CADASTRO DE REAGENTE/SOLUÇÃO"
    ])

    with aba_protocolo:
        with st.form("form_protocolo"):
            nome = st.text_input("Nome do Protocolo")
            grupo = st.text_input("Grupo ou Área")

            categoria = st.selectbox("Categoria do Protocolo", [
                "Extração de DNA", "Extração de RNA", "Cultivo Celular",
                "Transfecção", "Diferenciação Celular", "Outro"
            ])
            versao = st.text_input("Versão", value="1.0")
            data = st.date_input("Data de Criação", value=datetime.today())
            validade = st.date_input("Validade do Protocolo")

            autor = st.text_input("Nome do Autor")
            email = st.text_input("E‑mail")
            departamento = st.text_input("Departamento")
            cargo = st.text_input("Cargo")

            opcoes = [r["nome"] for r in st.session_state.get("reagentes", [])]
            reagentes_usados = st.multiselect("Reagentes Utilizados", opcoes)

            st.markdown("### 📑 Protocolo")
            st.info("""
            Carregue o protocolo em **formato PDF** para leitura.
            Adicione também o arquivo Word em **Anexos Adicionais**.
            """)

            arquivo = st.file_uploader(
                "Anexar protocolo (PDF obrigatório)",
                type=["pdf"]
            )

            st.markdown("### 🔗 Referência do Protocolo")
            ref_autor = st.text_input("Nome do Autor da Referência")
            ref_ano = st.text_input("Ano da Publicação")
            ref_doi = st.text_input("DOI")
            ref_link = st.text_input("Link (HTML)")

            st.markdown("### 📎 Anexos Adicionais")
            st.file_uploader(
                "Anexar outros arquivos (WORD original obrigatório)",
                type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "xlsx", "csv"],
                key="anexos_adicionais_protocolo"
            )

            submitted = st.form_submit_button("💾 Salvar Protocolo")
            if submitted:
                novo = {
                    "id": str(uuid.uuid4())[:8],
                    "nome": nome.upper(),
                    "grupo": grupo.upper(),
                    "categoria": categoria.upper(),
                    "versao": versao.upper(),
                    "data": data.strftime("%Y-%m-%d"),
                    "validade": validade.strftime("%Y-%m-%d"),
                    "autor": autor.upper(),
                    "email": email.upper(),
                    "departamento": departamento.upper(),
                    "cargo": cargo.upper(),
                    "reagentes": ", ".join(reagentes_usados),
                    "arquivo_nome": arquivo.name if arquivo else None,
                    "arquivo_bytes": arquivo.read() if arquivo else None,
                    "historico": [],
                    "referencia": {
                        "autor": ref_autor.upper(),
                        "ano": ref_ano.upper(),
                        "doi": ref_doi.upper(),
                        "link": ref_link.upper()
                    },
                    "comentarios": []
                }

                df_novo = pd.DataFrame([novo])
                st.session_state.dados = pd.concat([st.session_state.dados, df_novo], ignore_index=True)
                st.success("✅ Protocolo cadastrado com sucesso!")

    # ABA REAGENTE
    with aba_reagente:
        with st.form("form_reagente"):
            nome_sol = st.text_input("Nome da Solução/Reagente")

            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                comp = st.text_input("Componente")
            with col2:
                conc = st.text_input("Concentração")
            with col3:
                unidade = st.selectbox("Unidade", ["%", "mL", "µL", "mg/mL", "g/L", "outro"])

            st.markdown("### 📑 **Protocolo do reagente (PDF)**")
            st.info("""
            Carregue o protocolo do reagente em **formato PDF** para leitura.
            Adicione também o Word original em **Anexos Adicionais**.
            """)

            arquivo = st.file_uploader(
                "Anexar protocolo de preparo (PDF obrigatório)",
                type=["pdf"]
            )

            validade_reag = st.date_input("Validade da Solução")
            responsavel = st.text_input("Responsável pelo Preparo")
            local = st.text_input("Armazenamento/ Localização")

            st.markdown("### 📎 **Anexos Adicionais**")
            st.file_uploader(
                "Anexar outros arquivos (WORD original obrigatório)",
                type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "xlsx", "csv"],
                key="anexos_adicionais_reagente"
            )

            enviar = st.form_submit_button("💾 Salvar Reagente/Solução")
            if enviar:
                if "reagentes" not in st.session_state:
                    st.session_state.reagentes = []

                st.session_state.reagentes.append({
                    "nome": nome_sol.upper(),
                    "componentes": f"{comp.upper()} – {conc.upper()} {unidade}",
                    "preparo": "",  # Não estamos usando o campo `preparo` em rich text aqui
                    "validade": validade_reag.strftime("%Y-%m-%d"),
                    "responsavel": responsavel.upper(),
                    "local": local.upper(),
                    "arquivo_nome": arquivo.name if arquivo else None,
                    "arquivo_bytes": arquivo.read() if arquivo else None
                })

                st.success("✅ Reagente/Solução cadastrada!")
