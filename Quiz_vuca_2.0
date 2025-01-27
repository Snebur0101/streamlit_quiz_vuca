import  streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit_authenticator as stauth
import matplotlib.pyplot as plt
import secrets

from streamlit import success

from Quiz_vuca import respostas

cred = credentials.cerificate("credenciais_quiz.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

nomes = ['Marcos', 'Davi', 'Felipe', 'Hiago', 'Ismael', 'Jônatas', 'Levi', 'Márcio', 'Pedro', 'Rubens', 'Tiago']
usuarios = ['criador', 'respondente','respondente','respondente','respondente','respondente','respondente','respondente','respondente','respondente','respondente']
senhas =  ['Torchic123', 'Davi123', 'Felipe123', 'Hiago123', 'Ismael123', 'Jônatas123', 'Levi123', 'Márcio123', 'Pedro123', 'Rubens123', 'Tiago123']
hashed_senhas = stauth.Hasher(senhas).generate()

cookie_name = "meu_cookie_auth"
random_key = secrets.token_hex(16)
autenticador = stauth.Authenticate(nomes, usuarios, hashed_senhas, 'cookie_name', 'random_key')
nome, authentication_status, usuarios = autenticador.login('Login','sidebar')

if authentication_status is True:
    if usuarios == 'criador':
        st.markdown('## Crie as perguntas do Quiz')
        pergunta = st.text_input('Digite a pergunta')
        respostas = st.text_input('Difite as opçãode de resposta (separe elas por ponto e vírgula').split(';')
        gabarito = st.text_input('Resposta correta (presica que a respota esteja escrita por extenso)')

        if st.button('Salvar Respota'):
            if pergunta and respostas and gabarito:
                data = {
                    'pergunta': pergunta,
                    'respostas': respostas,
                    'gabarito': gabarito
                }
                db.collection('perguntas').add(data)
                st;success('Pergunta foi salva com sucesso!')
            else:
                st.error('Algum campo não foi preenchido, verifique novamente se todos os campos foram preenchidos!')
    elif usuarios == 'respondente':
        st.markdown('Responda todas as perguntas abaixo:')

        pergunta_ref = db.collection('perguntas'),stream()
        pergunta = [{'id': p.id, **p.to_dict()} for p in pergunta_ref]
        
        if perguntas:
            for i, pergunta in enumerate(perguntas):
                st.markdown(f'### Pergunta {i + 1}: {pergunta['pergunta']}')
                respostas = st.selectbox('Escolha uma opçao', pergunta[respostas], key=pergunta['id'])
                
                
