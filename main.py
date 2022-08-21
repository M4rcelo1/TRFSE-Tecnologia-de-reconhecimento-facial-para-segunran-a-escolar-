import json
from PySimpleGUI import PySimpleGUI as sg
import Coletor_de_dados as cd
import cv2
import numpy as np

sg.theme('DarkGrey4')
screen_size = (600, 600)
background_color = "#13293d"
logo = "imagens/logo.png"

data_path = 'data.json'  # Caminho para a base de dados
admin = {
    "user0": [
    "0",
    "Admin",
    "0",
    "0",
    "0"
  ]
}

def save_data(file):  # Reliza o salvamento na base de dados
    with open(data_path, "w", encoding="utf-8") as data:
        save = json.dump(file, data, indent=2, separators=(",", ": "), sort_keys=True)
        return save

def load_data(name_json):  # Puxa os dados da base de dados
    try:
        with open(name_json, "r", encoding="utf-8") as data:
            return json.load(data)
    except:
        save_data(admin)

def update_data(id, name, cpf, rg, matricula):  # Atualiza os dados da base
    list = []
    list.append(id)
    list.append(name)
    list.append(cpf)
    list.append(rg)
    list.append(matricula)
    try:
        data = load_data(data_path)
        data[f'user{id}'] = list
        save_data(data)
    except:
        save_data(admin)
        data = load_data(data_path)
        save_data(data)
        data[f'user{id}'] = list
        save_data(data)

def same_users(id, nome, cpf, rg, matricula):  # Faz a verificação para não ocorrer redundancia
    result = True
    data = load_data(data_path)
    for u in data:
        item = data[u]
        if str(id) == str(item[0]):
            if id == 'Não cadastrado':
                continue
            else:
                result = False
                error_page('OPS... Parece que esse id já está cadastrado em nosso banco de dados, tente novamente com um diferente')
                break
        # if str(nome) == str(item[1]):
            # if cpf == 'Não cadastrado':
                # continue
            # else:
                # result = False
                # error_page('OPS... Parece que esse nome já está cadastrado em nosso banco de dados, tente novamente com um diferente')
                # break
        if str(cpf) == str(item[2]):
            if cpf == 'Não cadastrado':
                continue
            else:
                result = False
                error_page('OPS... Parece que esse cpf já está cadastrado em nosso banco de dados, tente novamente com um diferente')
                break
        if str(rg) == str(item[3]):
            if rg == 'Não cadastrado':
                continue
            else:
                result = False
                error_page('OPS... Parece que esse rg já está cadastrado em nosso banco de dados, tente novamente com um diferente')
                break
        if str(matricula) == str(item[4]):
            if cpf == 'Não cadastrado':
                continue
            else:
                result = False
                error_page('OPS... Parece que essa matrícula já está cadastrada em nosso banco de dados, tente novamente com uma diferente')
                break
    if result:
        update_data(id, nome, cpf, rg, matricula)
        photo_record_page(id)

def consult_by_name(name):  # Faz uma busca no banco de dados a partir do nome
    result = True
    data = load_data(data_path)
    for u in data:
        item = data[u]
        if item[1] == name:
            result = False
            query_result(item[0], item[1], item[2], item[3], item[4])
            break

    if result:
        error_page('Nem um usuário com esse nome encontrado no nosso banco de dados, tente com um nome diferente!')


def delete_user(id):  # Apaga um usuário da base de dados a partir do seu id
    try:
        data = load_data(data_path)
        del data[f'user{id}']
        save_data(data)
        sucess('Usuário deletado do banco de dados com sucesso!')
    except:
        error_page('O id digitado não foi encontrado em nosso banco de dados, tente um diferente!')

def home_page():  # Pagina inicial do programa
    layout = [
        [sg.Text(size=(10, 5), background_color=background_color), sg.Text('Seja Bem Vindo', size=(40, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=(22, 5), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Button('Cadastrar', size=(200, 0), font=('underline', 20), button_color='#006494')],
        [sg.Button('Consultar', size=(200, 0), font=('underline', 20), button_color='#006494')],
        [sg.Button('Deletar', size=(200, 0), font=('underline', 20), button_color='#006494')],
        [sg.Button('Sair', size=(200, 0), font=('underline', 20), button_color='#006494')],
    ]

    window = sg.Window('Tela de cadastro', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        if events == 'Cadastrar':
            window.close()
            record_page()
            break
        elif events == 'Consultar':
            window.close()
            consultation_page()
            break
        elif events == 'Deletar':
            window.close()
            delete_page()
            break
        elif events == 'Sair':
            window.close()
            break

def record_page():  # pagina de registro
    layout = [
        [sg.Text(size=(20, 5), background_color=background_color), sg.Text('Resgistar', size=(30, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 200))],
        [sg.Text('ID', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='id', size=(60, 2))],
        [sg.Text('Nome', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='name', size=(60, 2))],
        [sg.Text('CPF', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='cpf', size=(60, 2))],
        [sg.Text('RG', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='rg', size=(60, 2))],
        [sg.Text('Matrícula', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='matricula', size=(60, 2))],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text(size=(2, 0), background_color=background_color), sg.Button('Voltar', size=(9, 0), font=('underline', 15), button_color="#006494"), sg.Text(size=(35, 0), background_color=background_color), sg.Button('Cadastrar', size=(9, 0), font=('underline', 15), button_color="#006494") ]
    ]

    window = sg.Window('Tela de Registro', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cadastrar':
            window.close()
            id = value['id']
            name = value['name']
            cpf = value['cpf']
            rg = value['rg']
            matricula = value['matricula']

            if id == '':
                id = 'Não cadastrado'
            if name == '':
                name = 'Não cadastrado'
            if cpf == '':
                cpf = 'Não cadastrado'
            if rg == '':
                rg = 'Não cadastrado'
            if matricula == '':
                matricula = 'Não cadastrado'

            print(id, name, cpf, rg, matricula)
            same_users(id, name, cpf, rg, matricula)
            break
        elif events == 'Voltar':
            window.close()
            home_page()
            break

def consultation_page():  # Pagina de consulta
    layout = [
        [sg.Text(size=(20, 0), background_color=background_color), sg.Text('Consultar', size=(30, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text('Nome', size=(7, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='name', size=(60, 2))],
        [sg.Text(size=((0, 7)), background_color=background_color)],
        [sg.Text(size=(2, 0), background_color=background_color), sg.Button('Voltar', size=(9, 0), font=('underline', 15), button_color="#006494"), sg.Text(size=(35, 0), background_color=background_color), sg.Button('Consultar', size=(9, 0), font=('underline', 15), button_color="#006494")]
    ]

    window = sg.Window('Tela de Consulta', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Consultar':
            window.close()
            consult_by_name(value['name'])
            break
        elif events == 'Voltar':
            window.close()
            home_page()
            break

def user_photo(name):  # puxa a foto do usuario no banco de dados
    try:
        img = cv2.imread(f'perfils_usuarios/{name}.png')
        res = cv2.resize(img, dsize=(200, 200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f'perfils_usuarios/{name}.png', res)
        photo = f'perfils_usuarios/{name}.png'
    except:
        photo = 'perfils_usuarios/nao_registrado.png'
    return photo


def query_result(id, nome, cpf, rg, matricula):  # Resultado da conosulta
    layout = [
        [sg.Text(size=(2, 0), background_color=background_color), sg.Text('Resultado da consulta', size=(30, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(user_photo(nome), background_color=background_color, size=(200, 200))],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'ID: {id}', background_color=background_color, font=('underline', 15), text_color="#fff", size=(50, 0))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'Nome: {nome}', background_color=background_color, font=('underline', 15), text_color="#fff", size=(50, 0))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'CPF: {cpf}', background_color=background_color, font=('underline', 15), text_color="#fff", size=(50, 0))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'RG: {rg}', background_color=background_color, font=('underline', 15), text_color="#fff", size=(50, 0))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'Matrícula: {matricula}', background_color=background_color, font=('underline', 15), text_color="#fff", size=(50, 1))],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text(size=(2, 0), background_color=background_color), sg.Button('Voltar', size=(10, 0), font=('underline', 15), button_color="#006494")]
    ]

    window = sg.Window('Resultado da Consulta', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Voltar':
            window.close()
            consultation_page()
            break

def delete_page():  # Pagina de delete
    layout = [
        [sg.Text(size=(0, 1), background_color=background_color)],
        [sg.Text(size=(24, 0), background_color=background_color), sg.Text('Deletar', size=(30, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Text(size=((0, 1)), background_color=background_color)],
        [sg.Text('ID', size=(3, 1), font=('underline', 20), text_color="#fff", background_color=background_color), sg.Input(key='id', size=(10, 10))],
        [sg.Text(size=((0, 5)), background_color=background_color)],
        [sg.Text(size=(2, 0), background_color=background_color), sg.Button('Voltar', size=(9, 0), font=('underline', 15), button_color="#006494"), sg.Text(size=(35, 0), background_color=background_color), sg.Button('Deletar', size=(9, 0), font=('underline', 15), button_color="#006494")]
    ]

    window = sg.Window('Tela de Consulta', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Deletar':
            window.close()
            delete_user(value['id'])
            break
        elif events == 'Voltar':
            window.close()
            home_page()
            break

def error_page(menssagem):  # Pagina de erro
    layout = [
        [sg.Text(size=(24, 0), background_color=background_color), sg.Text('ERRO', size=(30, 1), font=('underline', 40), text_color="#ff0000", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'  {menssagem}', background_color=background_color, font=('underline', 15), text_color="#ff0000", size=(50, 0))],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(10, 1), background_color=background_color), sg.Button('Tentar Novamente', size=(30, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('ERRO', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Tentar Novamente':
            window.close()
            home_page()
            break

def photo_record_page(id):  # Pagina de preparo para tirar as fotos
    layout = [
        [sg.Text(size=(18, 0), background_color=background_color), sg.Text('Tirar fotos', size=(30, 1), font=('underline', 40), text_color="#fff", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Text(size=(5, 1), background_color=background_color), sg.Text(f'Tudo Pronto para tirar as fotos ', background_color=background_color, font=('underline', 25), text_color="#fff", size=(50, 0))],
        [sg.Text(size=(5, 1), background_color=background_color), sg.Text(f'para o cadastro?', background_color=background_color, font=('underline', 25), text_color="#fff", size=(50, 0))],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color), sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"), sg.Text(size=(30, 1), background_color=background_color), sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            face_center(id)
            break

def face_center(id):
    layout = [
        [sg.Text(size=(2, 1), background_color=background_color), sg.Image('imagens/face_center.png', background_color=background_color)],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color), sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"), sg.Text(size=(30, 1), background_color=background_color),sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            cd.program(id)
            return True

def face_right():
    layout = [
        [sg.Text(size=(2, 1), background_color=background_color),
         sg.Image('imagens/face_right.png', background_color=background_color)],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color),
         sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"),
         sg.Text(size=(30, 1), background_color=background_color),
         sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            return True

def face_left():
    layout = [
        [sg.Text(size=(2, 1), background_color=background_color),
         sg.Image('imagens/face_left.png', background_color=background_color)],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color),
         sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"),
         sg.Text(size=(30, 1), background_color=background_color),
         sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            return True

def face_up():
    layout = [
        [sg.Text(size=(2, 1), background_color=background_color),
         sg.Image('imagens/face_up.png', background_color=background_color)],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color),
         sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"),
         sg.Text(size=(30, 1), background_color=background_color),
         sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            return True

def face_down():
    layout = [
        [sg.Text(size=(2, 1), background_color=background_color),
         sg.Image('imagens/face_down.png', background_color=background_color)],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(1, 1), background_color=background_color),
         sg.Button('Cancelar', size=(10, 0), font=('underline', 17), button_color="#006494"),
         sg.Text(size=(30, 1), background_color=background_color),
         sg.Button('Continuar', size=(10, 0), font=('underline', 17), button_color="#006494")]
    ]

    window = sg.Window('Tirar fotos', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Cancelar':
            window.close()
            home_page()
            break
        elif events == 'Continuar':
            window.close()
            return True

def sucess(menssagem):  # Pagina para mostrar menssagem de sucesso
    layout = [
        [sg.Text(size=(21, 0), background_color=background_color), sg.Text('Sucesso', size=(30, 1), font=('underline', 40), text_color="#00d315", background_color=background_color)],
        [sg.Text(size=(22, 1), background_color=background_color), sg.Image(logo, background_color=background_color, size=(200, 250))],
        [sg.Text(expand_x=True, background_color=background_color), sg.Text(f'  {menssagem}', background_color=background_color, font=('underline', 15), text_color="#00d315", size=(50, 0))],
        [sg.Text(background_color=background_color, expand_y=True)],
        [sg.Text(size=(5, 1), background_color=background_color), sg.Button('Voltar', size=(30, 0), font=('underline', 20), button_color="#006494")]
    ]

    window = sg.Window('ERRO', layout, size=screen_size, background_color=background_color)

    while True:
        events, value = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        elif events == 'Voltar':
            window.close()
            home_page()
            break

if __name__ == "__main__":
    home_page()