import PySimpleGUI as sg
import sqlite3


connection = sqlite3.connect('alunos.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS alunos(ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf INTEGER, disciplina TEXT, nota INTEGER)')
connection.close()
