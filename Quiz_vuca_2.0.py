import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit_authenticator as stauth
import matplotlib.pyplot as plt
import hashlib

if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais_quiz.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

nomes = ['Marcos', 'Davi', 'Felipe', 'Hiago', 'Ismael', 'Jônatas', 'Levi', 'Márcio', 'Pedro', 'Rubens', 'Tiago']
usuarios = ['criador', 'respondente', 'respondente', 'respondente', 'respondente', 'respondente', 'respondente',
            'respondente', 'respondente', 'respondente', 'respondente']
senhas = ['Torchic123', 'Davi123', 'Felipe123', 'Hiago123', 'Ismael123', 'Jônatas123', 'Levi123', 'Márcio123', 
          'Pedro123', 'Rubens123', 'Tiago123']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

hashed_senhas = [hash_password(senha) for senha in senhas]

cookie_name = "meu_cookie_auth"
random_key = "chave_aleatoria"
autenticador = stauth.Authenticate(nomes, usuarios, hashed_senhas, cookie_name, random_key)

nome, authentication_status, usuario = autenticador.login('Login', 'sidebar')

if authentication_status:
    st.write(f"Olá {nome}, você está autenticado como {usuario}.")
else:
    st.write("Falha na autenticação!")

if authentication_status is True:
    if usuario == 'criador':
        st.markdown('## Crie as perguntas do Quiz')
        pergunta = st.text_input('Digite a pergunta')
        respostas = st.text_input('Digite as opções de resposta (separe elas por ponto e vírgula)').split(';')
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
                st.error('Algum campo não foi preenchido, verifique novamente se todos os campos foram preenchidos!')
    elif usuario == 'respondente':
        st.markdown('Responda todas as perguntas abaixo:')

        pergunta_ref = db.collection('perguntas').stream()
        perguntas = [{'id': p.id, **p.to_dict()} for p in pergunta_ref]

        if perguntas:
            for i, pergunta in enumerate(perguntas):
                st.markdown(f'### Pergunta {i + 1}: {pergunta["pergunta"]}')
                resposta = st.selectbox('Escolha uma opção', pergunta['respostas'], key=pergunta['id'])
