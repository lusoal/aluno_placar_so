from flask import Flask, render_template, jsonify, \
    request, Response, redirect, url_for, session

from controller.UserController import user_controller

#Validar a sessao
def validate_session(session):
    print(session.get('username'))
    if session.get('username'):
        return True
    else:
        return False

#Flask Configurations
class FlaskConfs():
    
    #Atributos
    app = Flask(__name__)
    app.secret_key = 'eipohgoo4rai0uf5ie1oshahmaeF'

    def __call__(self):
        self.register_blue_prints()
        self.run_app()
    
    def register_blue_prints(self):
        self.app.register_blueprint(user_controller)

    def run_app(self):
        self.app.run(debug=True, host='0.0.0.0')