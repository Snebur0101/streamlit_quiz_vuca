import streamlit as st
import json
import os

# Função para carregar perguntas de um arquivo JSON
def carregar_perguntas(nome_json):
    try:
        with open(nome_json, 'r', encoding='utf-8') as file:
            perguntas = json.load(file)
    except FileNotFoundError:
        st.error(f'O arquivo {nome_json} não foi encontrado!')
        perguntas = []
    return perguntas

# Arquivo JSON onde as perguntas estão armazenadas
nome_json = 'perguntas.json'

# Carregar as perguntas
questions = carregar_perguntas(nome_json)

# Se o arquivo JSON estiver vazio ou não encontrado, a variável 'questions' ficará vazia
if not questions:
    st.error('Não há perguntas carregadas.')

# Definir as variáveis para pontuação e feedback
score = 0
feedback = []
user_answers = {}

# Título do quiz
st.title('Quiz de conhecimentos gerais do sistema VUCA')

# Seleção do nome do usuário
nome_usuario = st.selectbox(
    'Quem está respondendo?',
    ('', 'Davi', 'Felipe', 'Hiago', 'Ismael', 'Jônatas', 'Levi', 'Marcos', 'Márcio', 'Pedro', 'Rubens', 'Tiago'),
)

# Cabeçalho das perguntas
st.header('Perguntas')
st.subheader('Responda todas as perguntas abaixo:')

# Loop pelas perguntas carregadas do arquivo JSON
for i, q in enumerate(questions, 1):
    st.markdown(f'**Pergunta {i}: {q["question"]}**')

    # Caixa de seleção para as respostas
    user_answer = st.selectbox('', q['options'], key=f'question_{i}_radio')

    user_answers[f'Pergunta {i}'] = user_answer

    # Verificar se a resposta está correta
    if user_answer in q['correct_answers']:
        score += 1
        feedback.append(f'✅ Pergunta {i}: Resposta correta!')
    else:
        feedback.append(f'❌ Pergunta {i}: Resposta errada!')

# Quando o usuário clicar no botão "Terminar o quiz"
if st.button('Terminar o quiz'):
    st.title('Respostas do usuário:')
    for i, fb in enumerate(feedback, 1):
        st.write(f'Pergunta {i}: {fb}')
    st.write(f'A sua pontuação foi: {score}')

# Salvar os resultados no arquivo JSON
nome_csv = 'Respostas_quiz.csv'
cabecalho = ['Nome do usuário'] + [f'Pergunta {i}' for i in range(1, len(questions) + 1)] + ['Pontuação']

if nome_usuario.lower() == 'marcos':
    with open(nome_csv, mode='a', newline='', encoding='utf-8') as file:
        respostas = {
            'nome_usuario': nome_usuario,
            'pontuacao': score,
            'respostas': user_answers
        }

        # Abrir ou criar o arquivo JSON de respostas
        if os.path.exists(nome_json):
            with open(nome_json, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = []

        data.append(respostas)

        # Gravar os dados de respostas no arquivo JSON
        with open(nome_json, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Download do arquivo JSON com as respostas
        with open(nome_json, 'rb') as f:
            st.download_button(
                label="Baixar Respostas",
                data=f,
                file_name=nome_json,
                mime="application/json"
            )