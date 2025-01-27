import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

if not firebase_admin._apps:
    cred = credentials.Certificate("quiz-b3987-firebase-adminsdk-fbsvc-35d25b830f.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def obter_tipo_usuario(nome_usuario):
    user_ref = db.collection('usuarios').document(nome_usuario)
    user_doc = user_ref.get()

    if user_doc.exists:
        return user_doc.to_dict().get('tipo')
    else:
        return None

st.sidebar.title("Escolha uma opção:")
opcao = st.sidebar.radio("Ação", ["Login", "Registrar"])

if opcao == "Registrar":
    st.title("Registrar Novo Usuário")

    novo_usuario = st.text_input("Digite o nome de usuário:")
    setor = st.selectbox('Selecione o setor do usuário:', ['Suporte','Implantação','CX'])
    nova_senha = st.text_input("Digite a senha:", type="password")
    tipo_usuario = st.selectbox("Selecione o tipo de usuário:", ["criador", "respondente"])

    if st.button("Registrar"):
        if novo_usuario and nova_senha and tipo_usuario and setor:
            user_ref = db.collection('usuarios').document(novo_usuario)

            if user_ref.get().exists:
                st.error("Usuário já existe! Escolha outro nome.")
            else:
                data = {
                    'nome': novo_usuario,
                    'setor': setor,
                    'senha': hash_password(nova_senha),
                    'tipo': tipo_usuario
                }
                user_ref.set(data)
                st.success("Usuário registrado com sucesso!")
        else:
            st.error("Todos os campos são obrigatórios!")

elif opcao == "Login":
    st.title("Login")

    nome_usuario = st.text_input('Digite o seu nome de usuário')
    senha_usuario = st.text_input('Digite sua senha', type='password')

    if st.button("Entrar"):
        if nome_usuario and senha_usuario:
            user_ref = db.collection('usuarios').document(nome_usuario)
            user_doc = user_ref.get()

            if user_doc.exists:
                dados_usuario = user_doc.to_dict()
                senha_hash = hash_password(senha_usuario)

                if senha_hash == dados_usuario['senha']:
                    tipo_usuario = dados_usuario['tipo']

                    if tipo_usuario == 'criador':
                        st.markdown('## Crie as perguntas do Quiz')
                        pergunta = st.text_input('Digite a pergunta')
                        respostas = st.text_input(
                            'Digite as opções de resposta (separe elas por ponto e vírgula)').split(';')
                        gabarito = st.text_input('Resposta correta (precisa que a resposta esteja escrita por extenso)')

                        if st.button('Salvar Resposta'):
                            if pergunta and respostas and gabarito:
                                data = {
                                    'pergunta': pergunta,
                                    'respostas': respostas,
                                    'gabarito': gabarito
                                }
                                db.collection('perguntas').add(data)
                                st.success('Pergunta foi salva com sucesso!')
                            else:
                                st.error(
                                    'Algum campo não foi preenchido, verifique novamente se todos os campos foram preenchidos!')
                    elif tipo_usuario == 'respondente':
                        st.markdown('Responda todas as perguntas abaixo:')

                        pergunta_ref = db.collection('perguntas').stream()
                        perguntas = [{'id': p.id, **p.to_dict()} for p in pergunta_ref]

                        if perguntas:
                            for i, pergunta in enumerate(perguntas):
                                st.markdown(f'### Pergunta {i + 1}: {pergunta["pergunta"]}')
                                resposta = st.selectbox('Escolha uma opção', pergunta['respostas'], key=pergunta['id'])
                else:
                    st.error("Senha incorreta!")
            else:
                st.error("Usuário não encontrado!")
        else:
            st.error("Todos os campos são obrigatórios!")
