import streamlit as st
import datetime
import uuid
import pandas as pd

def exibir_formulario():
    df = st.session_state.dados

    st.subheader("Cadastro de novo protocolo")

    # Autocomplete com sugestão de nomes já cadastrados
    nomes_existentes = df["nome"].dropna().unique().tolist()
    nome = st.text_input("Nome do protocolo", placeholder="Digite ou selecione um nome já existente")

    if nome:
        similares = [n for n in nomes_existentes if nome.lower() in n.lower()]
        if similares:
            st.info(f"⚠️ Já existe protocolo com nome semelhante. Versões existentes: {', '.join(similares)}")

    grupo = st.selectbox("Grupo responsável", ["GRUPO CARDIO", "GRUPO TRONCO", "GRUPO MARCO", "OUTRO"])

    # Tipo de protocolo define a categoria
    categoria = st.selectbox("Tipo de protocolo", ["🔬 Protocolo Laboratorial", "🧪 Protocolo de Reagentes/Soluções"])

    validade = st.date_input("Validade", value=datetime.date.today())
    autor = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    cargo = st.text_input("Cargo")
    conteudo = st.text_area("Conteúdo do protocolo", height=200)

    # Campo reagentes necessários (filtrar apenas se houver reagentes cadastrados)
    reagentes_df = df[df["categoria"] == "🧪 Protocolo de Reagentes/Soluções"]
    reagentes_opcoes = reagentes_df["nome"].unique().tolist()
    reagentes = st.multiselect("Reagentes necessários", reagentes_opcoes)

    # Upload de arquivo (PDF, imagem, docx, xlsx, etc.)
    arquivo = st.file_uploader("Anexar arquivo (PDF, imagem, Word, Excel, etc.)", type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "xlsx", "csv"])

    enviar = st.button("Salvar protocolo")

    if enviar:
        if not nome or not autor or not conteudo:
            st.warning("Por favor, preencha os campos obrigatórios.")
            return

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
            "departamento": "",  # campo descontinuado
            "cargo": cargo,
            "conteudo": conteudo,
            "reagentes": reagentes,
            "arquivo_nome": arquivo.name if arquivo else "",
            "arquivo_bytes": arquivo.read() if arquivo else None,
            "historico": historico
        }

        novo_df = pd.DataFrame([novo])
        st.session_state.dados = pd.concat([df, novo_df], ignore_index=True)

        st.success(f"✅ Protocolo '{nome}' salvo como versão {versao}.")
