import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

from Quiz_vuca import nome_usuario

if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais_quiz.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def obter_tipo_usuario(nome_usuario):
    user_ref = db.collection('usuarios').document(nome_usuario)
    user_doc = user_ref.get()

    if user_doc.exists:
        return user_doc.to_dict().get('tipo')
    else:
        return None 
    
nome_usuario = st.text_input('Digite o seu nome de usuário')

if nome_usuario:
    tipo_usuario = obter_tipo_usuario(nome_usuario)
    
    if tipo_usuario == 'criador':
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
    elif tipo_usuario == 'respondente':
        st.markdown('Responda todas as perguntas abaixo:')

        pergunta_ref = db.collection('perguntas').stream()
        perguntas = [{'id': p.id, **p.to_dict()} for p in pergunta_ref]

        if perguntas:
            for i, pergunta in enumerate(perguntas):
                st.markdown(f'### Pergunta {i + 1}: {pergunta["pergunta"]}')
                resposta = st.selectbox('Escolha uma opção', pergunta['respostas'], key=pergunta['id'])
