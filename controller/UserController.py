from flask import Flask, render_template, jsonify, \
    request, Response, redirect, url_for, session, Blueprint
import os

import flask_confs
from model.User import User
from service.UserSevice import UserService  
#Atributo
user_controller = Blueprint('user_controller', __name__)
userService = UserService()

@user_controller.route('/', methods=['GET'])
def index():
    return redirect(url_for('user_controller.login'))

@user_controller.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = User(username, password)
        try:
            if (userService.realizar_login(usuario)):
                session['user_id'] = usuario.id
                session['username'] = usuario.username
                return redirect(url_for("user_controller.user_home"))
            else:
                return redirect(url_for('user_controller.login'))
        except Exception as e:
            return redirect(url_for('user_controller.login'))
    else:
        return render_template("login.html")

@user_controller.route('/user_home/', methods=['GET'])
def user_home():
    if not flask_confs.validate_session(session):
        return redirect(url_for('user_controller.login'))
    print(session)
    pontuacao = userService.get_pontuacao_jogador(session['user_id'])
    session['pergunta_index'] = 0
    return render_template("user_index.html", pontuacao = pontuacao)

@user_controller.route('/iniciar_partida/', methods=['POST'])
def iniciar_partida():
    if not flask_confs.validate_session(session):
        return redirect(url_for('user_controller.login'))
    
    partida_id = request.form['partida']
    try:
        sessao_id = userService.iniciar_partida(partida_id, session['user_id'])
        session['sessao_id'] = sessao_id
        session['partida_id'] = partida_id
        print(session)
        return redirect(url_for('user_controller.get_pergunta'))
    except Exception as e:
        print(e)
        return redirect(url_for('user_controller.user_home'))

@user_controller.route('/perguntas/', methods=['GET'])
def get_pergunta():
    perguntas = userService.get_perguntas(session['partida_id'])
    pergunta = userService.define_pergunta(perguntas, session['pergunta_index'])
    if(pergunta):
        session['pergunta_index'] += 1
        print(F"INDICE DA PERGUNTA: {session['pergunta_index'] }")
        session['pergunta_rodada'] = pergunta
        return render_template("pergunta.html", pergunta = pergunta)
    else:
        session.pop('sessao_id')
        session.pop('partida_id')
        session.pop('pergunta_rodada')
        return redirect(url_for('user_controller.jogo_finalizado'))

@user_controller.route('/responder_pergunta/', methods=['POST'])
def responder_pergunta():
    escolha_pergunta = request.form['opt']
    print(f"RESPOSTA_ESCOLHIDA: {escolha_pergunta}")
    if escolha_pergunta == session['pergunta_rodada'].get('resposta'):
        #Pontuando corretamente a resposta
        userService.pontuar_sessao_usuario(session['sessao_id'])
        return redirect(url_for('user_controller.resposta_correta'))
    else:
        return redirect(url_for('user_controller.resposta_incorreta'))

@user_controller.route('/resposta_correta/', methods=['GET'])
def resposta_correta():
    valor_resposta = None
    for key, value in session['pergunta_rodada'].items():
        if "alternativa"+session['pergunta_rodada'].get("resposta") in key:
            valor_resposta = value
            break
    return render_template("resposta_correta.html", resposta = valor_resposta, pergunta = session['pergunta_rodada'])
    

@user_controller.route('/resposta_incorreta/', methods=['GET'])
def resposta_incorreta():
    valor_resposta = None
    for key, value in session['pergunta_rodada'].items():
        if "alternativa"+session['pergunta_rodada'].get("resposta") in key:
            valor_resposta = value
            break
    return render_template("resposta_incorreta.html", resposta = valor_resposta, pergunta = session['pergunta_rodada'])

@user_controller.route('/jogo_finalizado/', methods=['GET'])
def jogo_finalizado():
    if not flask_confs.validate_session(session):
        return redirect(url_for('user_controller.login'))
    return render_template("partida_finalizada.html")

@user_controller.route('/logout/', methods=['GET', 'POST'])
def logout():
    if not flask_confs.validate_session(session):
        return redirect(url_for('user_controller.login'))
    session.clear()
    return redirect(url_for('user_controller.login'))
