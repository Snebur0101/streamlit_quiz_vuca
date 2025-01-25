import streamlit as st
import csv

questions = [
    {
        'question': 'Qual é o status necessário para que uma venda do delivery seja considerada no caixa?',
        'options': ['Em Produção', 'Produzido', 'Finalizado', 'Aguardando'],
        'correct_answers': ['Finalizado']
    },
    {
        'question': 'Qual é a função do botão "FORÇAR ACEITE" na retaguarda?',
        'options': ['Cancelar pedidos no status Aguardando', 'Liberar pedidos travados no status Aguardando',
                    'Finalizar pedidos automaticamente', 'Emitir nota fiscal para pedidos pendentes'],
        'correct_answers': ['Liberar pedidos travados no status Aguardando']
    },
    {
        'question': 'Em qual aba o VUCAZAP deve ser configurado para envio de relatórios do fechamento de caixa?',
        'options': ['WHATSAPP', 'NOTIFICAÇÕES', 'DELIVERY', 'RELATÓRIOS'],
        'correct_answers': ['NOTIFICAÇÕES']
    },
    {
        'question': 'Qual configuração é necessária para permitir pedidos no delivery?',
        'options': ["RETAGUARDA > MENU > DELIVERY > ABA: CANAIS", "RETAGUARDA > PARÂMETROS > VUCAFOOD > ABA: FUNÇÕES",
                    "RETAGUARDA > MENU > UNIDADES > ABA: PAGAMENTOS",
                    "RETAGUARDA > PARÂMETROS > ESTOQUE > ABA: PRODUTOS"],
        'correct_answers': ['RETAGUARDA > PARÂMETROS > VUCAFOOD > ABA: FUNÇÕES']
    },
    {
        'question': 'Qual informação é necessária para que o salário base de um colaborador seja exibido na aba "Dados da Contabilidade?',
        'options': ['Vincular o colaborador a um regime de contratação',
                    'Aprovar o período de experiência do colaborador',
                    'Vincular o salário base na aba: Retaguarda > RH > Colaboradores > Editar > Aba: Salário',
                    'Ativar o checkbox "Pagar" na aba Banco de Horas'],
        'correct_answers': ['Vincular o salário base na aba: Retaguarda > RH > Colaboradores > Editar > Aba: Salário']
    },
    {
        'question': ' Onde é feito o cadastro inicial de um colaborador no sistema?',
        'options': ["Retaguarda > Parâmetros > RH > Colaboradores",
                    "Retaguarda > Menu > RH > Colaboradores > Campo: +Adicionar",
                    "Retaguarda > Menu > Gerenciamento > Controle de Ponto > Colaboradores",
                    "Frente de Loja > Menu > RH > Campo: Colaboradores"],
        'correct_answers': ['Retaguarda > Menu > RH > Colaboradores > Campo: +Adicionar']
    },
    {
        'question': 'O que acontece quando um colaborador anexa um atestado pelo sistema?',
        'options': ["O atestado é automaticamente aprovado e alimenta o controle de ponto.",
                    "O atestado precisa ser aprovado pelo RH para alimentar o controle de ponto",
                    "O atestado é apenas visualizado no perfil do colaborador",
                    "O sistema não permite anexar atestados diretamente pelo colaborador"],
        'correct_answers': ['O atestado precisa ser aprovado pelo RH para alimentar o controle de ponto']
    },
    {
        'question': 'Onde você deve definir a carga horária semanal de um colaborador para cálculo correto do banco de horas?',
        'options': ["RETAGUARDA > MENU > GERENCIAMENTO > CONTROLE DE PONTO",
                    "RETAGUARDA > MENU > FINANCEIRO > CONTAS A PAGAR", "PARÂMETROS > RH > ABA: CARGA HORÁRIA SEMANAL",
                    "PARÂMETROS > RH > ABA: ADICIONAL NOTURNO"],
        'correct_answers': ['PARÂMETROS > RH > ABA: CARGA HORÁRIA SEMANAL']
    },
    {
        'question': 'Qual das opções abaixo descreve corretamente quando utilizar o motivo "Freelancer para TERCEIROS" no relógio de ponto?',
        'options': ["Quando o colaborador está cumprindo sua própria carga horária",
                    "Quando um freelancer está substituindo um colaborador escalado para trabalhar",
                    "Quando um freelancer foi contratado diretamente pela casa",
                    "Quando o colaborador realiza uma pausa para intervalo"],
        'correct_answers': ['Quando um freelancer está substituindo um colaborador escalado para trabalhar']
    },
    {
        'question': 'Onde deve ser feita a vinculação/ficha técnica dos produtos de venda e produção própria para que haja baixa automática no estoque?',
        'options': ["Retaguarda > Menu > Compras > Ficha Técnica", "Retaguarda > Parâmetros > Estoque > Aba: Produtos",
                    "Retaguarda > Relatórios > Estoque > Ficha Técnica", "Retaguarda > Menu > Estoque > Parâmetros"],
        'correct_answers': ['Retaguarda > Parâmetros > Estoque > Aba: Produtos']
    },
    {
        'question': "Qual aba deve ser acessada para cadastrar os motivos de cancelamento dos pedidos?",
        'options': ["Retaguarda > Parâmetros > Estoque > Aba: Cancelamento",
                    "Retaguarda > Menu > Compras > Cancelamento",
                    "Retaguarda > Relatórios > Produtos > Aba: Cancelamento",
                    "Retaguarda > Estoque > Cancelamento > Motivos"],
        'correct_answers': ['Retaguarda > Parâmetros > Estoque > Aba: Cancelamento']
    },
    {
        'question': "O que ocorre ao ativar o checkbox 'Abrir comanda ao cadastrar novo Cartão Consumo'",
        'options': ["A tela retorna para o início, permitindo cadastrar um novo cartão",
                    "Abre diretamente a tela de lançamentos de produtos após cadastrar o cartão",
                    "Bloqueia a abertura de novas comandas no sistema",
                    "Permite o cadastro de um cartão sem a necessidade de preencher os dados do cliente"],
        'correct_answers': ['Abre diretamente a tela de lançamentos de produtos após cadastrar o cartão.']
    },
    {
        'question': 'O que ocorre ao ativar o checkbox "Ativar sincronização com Frente de Loja"?',
        'options': ['Os dados dos pedidos são armazenados apenas no tablet',
                    'Os lançamentos feitos pelo tablet são sincronizados automaticamente com o sistema de frente de loja',
                    'O tablet passa a operar de forma independente do sistema de frente de loja',
                    'Os pedidos enviados pelo tablet são excluídos ao sincronizar com o sistema'],
        'correct_answers': ['O tablet passa a operar de forma independente do sistema de frente de loja']
    },
    {
        'question': "Qual é o requisito básico para configurar uma impressora térmica via rede.",
        'options': ["Configurar a largura do papel diretamente no painel da impressora",
                    "Definir o endereço IP manualmente no sistema e no roteador",
                    "Garantir que a impressora esteja conectada à mesma rede do computador",
                    "Atualizar o firmware da impressora antes de conectá-la"],
        'correct_answers': ['Garantir que a impressora esteja conectada à mesma rede do computador']
    },
    {
        'question': "Durante a configuração de uma impressora de rede, qual procedimento é recomendado para verificar a conexão?",
        'options': ["Testar a impressão de um documento diretamente pelo painel da impressora",
                    "Executar um comando PING para o endereço IP da impressora",
                    "Substituir o cabo de energia por um modelo novo",
                    "Habilitar o DHCP para gerar automaticamente um IP dinâmico"],
        'correct_answers': ['Executar um comando PING para o endereço IP da impressora']
    },
    {
        'question': "Durante a configuração de uma impressora de rede, qual procedimento é recomendado para verificar a conexão?",
        'options': ["Testar a impressão de um documento diretamente pelo painel da impressora",
                    "Executar um comando PING para o endereço IP da impressora",
                    "Substituir o cabo de energia por um modelo novo",
                    "Habilitar o DHCP para gerar automaticamente um IP dinâmico"],
        'correct_answers': ['Executar um comando PING para o endereço IP da impressora']
    },
    {
        'question': "Como o adicional noturno é gerenciado no sistema?",
        'options': ["É automaticamente calculado com base nas horas trabalhadas no mês",
            "Deve ser cadastrado na aba Retaguarda > Parâmetros > RH > Aba: Adicional Noturno",
            "O colaborador insere manualmente suas horas de adicional noturno",
            "É calculado apenas no fechamento da folha de pagamento pelo financeiro"],
        'correct_answers': ['Deve ser cadastrado na aba Retaguarda > Parâmetros > RH > Aba: Adicional Noturno']
    },
]

score = 0

feedback = []

user_answers = {}

st.title('Quiz de conhecimentos gerais do sistema VUCA')

nome_usuario = st. selectbox(
    'Quem está respondendo?',
    ('','Davi', 'Felipe', 'Hiago', 'Ismael', 'Jônatas', 'Levi', 'Marcos', 'Márcio', 'Pedro', 'Rubens', 'Tiago'),
    )

st.header('Perguntas')
st.subheader('Responda todas as perguntas abaixo:')

for i, q in enumerate(questions, 1):
    st.markdown(f'**Pergunta {i}: {q['question']}**')

    user_answer =  st.radio('',q['options'],key=f'question_{i}_radio')

    user_answers[f'Pergunta {i}'] = user_answer

    if user_answer in q['correct_answers']:
        score += 1
        feedback.append(f'✅ Pergunta {i}: Resposta correta!')
    else:
        feedback.append(f'❌ Pergunta {i}: Respsota errada!')

if st.button('Terminar o quiz'):
    st.title('Respostas do usuário:')
    for i, fb in enumerate(feedback, 1):
        st.write(f'Pergunta {i}: {fb}')
    st.write(f'A sua pontuação foi: {score}')

nome_csv = 'Respotas_quiz.csv'
cabecalho = ['Nome do usuário'] + [f'Pergunta {i}' for i in range(1, len(questions) + 1)] + ['Pontuação']

if nome_usuario.lower() == 'marcos':
        with open(nome_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(cabecalho)

        row = [nome_usuario]

        for i in range(1, len(questions) + 1):
             row.append(user_answers.get(f'Pergunta {i}', ''))

        row.append(score)

        writer.writerow(row)

        with open(nome_csv, 'rb') as f:
            st.download_button(
            label="Baixar Respostas",
            data=f,
            file_name=nome_csv,
            mime="text/csv"
        )
