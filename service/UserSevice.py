import requests
import os
import json

class UserService(object):
    
    def realizar_login(self, user):
        payload = {'usuario': user.username, 'senha': ''}
        headers = {'content-type': "application/json"}
        try:
            response = requests.post(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/login/", 
                data=json.dumps(payload), headers=headers)
            if (response.status_code == 200):
                user.id = response.json().get('id')
                return response.json
            else:
                return False
        except Exception as e:
            print(e)
            raise e
    
    def iniciar_partida(self, partid_id, jogador_id):
        payload = {'partida_id': partid_id, 'jogador_id': jogador_id}
        headers = {'content-type': "application/json"}
        try:
            response = requests.post(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/sessao/", 
                data=json.dumps(payload), headers=headers)
            if (response.status_code == 200):
                sessao_id = response.json().get('sessao_id')
                print(f"SESSAO_ID: {sessao_id}")
                return sessao_id
            else:
                raise Exception('Nao existe partida')
        except Exception as e:
            raise e
    
    def get_perguntas(self, partid_id):
        headers = {'content-type': "application/json"}
        try:
            response = requests.get(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/partida/perguntas/{int(partid_id)}/"
                ,headers=headers)
            if (response.status_code == 200):
                print(response.json())
                return response.json()[0]
            else:
                raise Exception('Nao existe partida')
        except Exception as e:
            raise e
    
    def get_pontuacao_jogador(self, jogador_id):
        headers = {'content-type': "application/json"}
        try:
            response = requests.get(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/historico/pontuacao/{int(jogador_id)}/"
                ,headers=headers)
            if (response.status_code == 200):
                print(response.json())
                return response.json()
            else:
                raise Exception(response.json())
        except Exception as e:
            raise e
    
    def define_pergunta(self, perguntas, pergunta_index):
        print(f"PERGUNTA_INDICE: {pergunta_index}, PERGUNTA_LEN: {len(perguntas)}")
        if (pergunta_index >= len(perguntas)):
            return False
        else:
            return perguntas[pergunta_index]
    
    def pontuar_sessao_usuario(self, sessao_id):
        headers = {'content-type': "application/json"}
        try:
            response = requests.post(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/sessao/pontuar/{sessao_id}", 
            headers=headers)
            print(response.json())
        except Exception as e:
            raise e
    
    def realizar_logout(self, jogador_id):
        headers = {'content-type': "application/json"}
        payload = {'jogador_id': jogador_id}
        try:
            response = requests.post(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/logout/", 
            data=json.dumps(payload), headers=headers)
            print(response.json())
            if (response.status_code) == 200:
                return True
            else:
                False
        except Exception as e:
            raise e
    
    def get_partida_iniciada(self):
        headers = {'content-type': "application/json"}
        response = requests.get(f"http://{os.environ.get('URL_APPLICATION','localhost:8080')}/api/partida/iniciada/", 
            headers=headers)
        return response.json().get('message')