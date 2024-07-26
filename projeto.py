import PySimpleGUI as sg
import sqlite3

# Conectando ao banco de dados #
connection = sqlite3.connect('alunos.db')
cursor = connection.cursor()

# Criando a tabela #
cursor.execute('CREATE TABLE IF NOT EXISTS alunos(ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf INTEGER, ppg TEXT, ingresso TEXT)')

# Baixando os dados da tabela do banco de dados #
cursor.execute('SELECT * FROM alunos')
dados = cursor.fetchall()

# Desconectando do banco de dados #
connection.close()

# Criando a interface da aplicação #
titulos = ['ID', 'Nome', 'CPF', 'PPG', 'Ingresso']

def abrir_janela():
    sg.theme('DarkBlue4')

    layout = [
        [sg.Text(titulos[1]), sg.Input(size= 50 ,key= titulos[1])],
        [sg.Text(titulos[2]), sg.Input(size = 50, key= titulos[2])],
        [sg.Text(titulos[3]), sg.Combo(['Letras', 'Filosofia', 'Ciências Sociais'], key= titulos[3])],
        [sg.Text(titulos[4]), sg.Input(size = 50, key= titulos[4])],
        [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar', disabled=True), sg.Button('Excluir')],
        [sg.Table(dados, titulos ,key='tabela')],
        [sg.Button('Declaração de Matrícula')]
    ]

    return sg.Window('Emissor de Certificados - SIP', layout=layout, finalize=True, size=(400, 300))


janela = abrir_janela()

while True:
    event, values = janela.read()

    # Adição de novos itens à tabela #
    if event == 'Adicionar':
        # Reconectando ao banco de dados #
        connection = sqlite3.connect('alunos.db')
        cursor = connection.cursor()
        # Adicionando o novo item ao banco de dados #
        cursor.execute('INSERT INTO alunos (nome, cpf, ppg, ingresso) VALUES (?, ?, ?, ?)', (values['Nome'], values['CPF'], values['PPG'], values['Ingresso']))
        connection.commit()
        # Atualizando a tabela com os dados do banco de dados #
        cursor.execute('SELECT * FROM alunos')
        dados = cursor.fetchall()
        connection.close()
        # Requisitando o banco de dados para atualizar os dados da tabela #
        janela['tabela'].update(values=dados)
        # Limpando os inputs #
        for i in range(1, 5):
            janela[titulos[i]].update(value='')

    # Edição dos objetos já salvos #
    elif event == 'Editar':
        if values['tabela'] == []:
            sg.popup('Favor selecionar uma linha')
        else:
            # Preenchendo os inputs com os dados do objeto selecionado # 
            for i in range(1, 5):
                janela[titulos[i]].update(value=dados[values['tabela'][0]][i])    
            # Habilitando o botão 'Salvar' #
            janela['Salvar'].update(disabled=False)

    elif event == 'Salvar':
        # Reconectando ao banco de dados #
        connection = sqlite3.connect('alunos.db')
        cursor = connection.cursor()
        # Editando o objeto no banco de dados #
        cursor.execute('UPDATE alunos SET (nome, cpf, ppg, ingresso) = (?, ?, ?, ?) WHERE ID = ?', (values['Nome'], values['CPF'], values['PPG'], values['Ingresso'], dados[values['tabela'][0]][0]))
        connection.commit()
        # Atualizando a tabela com os dados do banco de dados #
        cursor.execute('SELECT * FROM alunos')
        dados = cursor.fetchall()
        connection.close()
        # Requisitando o banco de dados para atualizar os dados da tabela #
        janela['tabela'].update(values=dados)
        # Limpando os inputs #
        for i in range(1, 5):
            janela[titulos[i]].update(value='')

    elif event == 'Excluir':
        if values['tabela'] == []:
            sg.popup('Favor selecionar uma linha')
        else:
            # Reconectando ao banco de dados #
            connection = sqlite3.connect('alunos.db')
            cursor = connection.cursor()
            # Apagando o objeto no banco de dados #
            cursor.execute('DELETE FROM alunos WHERE ID = ?', str(dados[values['tabela'][0]][0]))
            connection.commit()
            # Atualizando a tabela com os dados do banco de dados #
            cursor.execute('SELECT * FROM alunos')
            dados = cursor.fetchall()
            connection.close()
            # Requisitando o banco de dados para atualizar os dados da tabela #
            janela['tabela'].update(values=dados)

    elif event == sg.WIN_CLOSED:
        break
