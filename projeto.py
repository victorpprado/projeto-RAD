import PySimpleGUI as sg
import sqlite3

# Conectando ao banco de dados #
connection = sqlite3.connect('alunos.db')
cursor = connection.cursor()

# Criando a tabela #
cursor.execute('CREATE TABLE IF NOT EXISTS alunos(ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf INTEGER, disciplina TEXT, nota INTEGER)')

# Baixando os dados da tabela do banco de dados #
cursor.execute('SELECT * FROM alunos')
dados = cursor.fetchall()

# Desconectando do banco de dados #
connection.close()

# Criando a interface da aplicação #
titulos = ['ID', 'Nome', 'CPF', 'Disciplina']

def abrir_janela():
    sg.theme('DarkTeal2')

    layout = [
        [sg.Text(titulos[1]), sg.Input(size = 30, key= titulos[1])],
        [sg.Text(titulos[2]), sg.Input(size = 14, key= titulos[2])],
        [sg.Text(titulos[3]), sg.Input(size = 30, key= titulos[3])],
        [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar', disabled=True), sg.Button('Excluir')],
        [sg.Table(dados, titulos ,key='tabela')],
        [sg.Button('Certificado')]
    ]

    return sg.Window('Emissor de Certificados - SIP', layout=layout, finalize=True)


janela = abrir_janela()

while True:
    event, values = janela.read()

    # Adição de novos itens à tabela #
    if event == 'Adicionar':
        # Reconectando ao banco de dados #
        connection = sqlite3.connect('alunos.db')
        cursor = connection.cursor()
        # Adicionando o novo item ao banco de dados #
        cursor.execute('INSERT INTO alunos (nome, cpf, disciplina) VALUES (?, ?, ?)', (values['Nome'], values['CPF'], values['Disciplina']))
        connection.commit()
        # Atualizando a tabela com os dados do banco de dados #
        cursor.execute('SELECT * FROM alunos')
        dados = cursor.fetchall()
        connection.close()
        # Limpando os inputs #
        for i in range(1, 4):
            janela[titulos[i]].update(value='')

    elif event == 'Editar':
        ...

    elif event == 'Salvar':
        ...

    elif event == sg.WIN_CLOSED:
        break
