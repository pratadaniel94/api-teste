from flask import Blueprint, make_response
import json


alunos = Blueprint('alunos', __name__, url_prefix="/alunos")

@alunos.route("")
def index():
    headers = {"content-type": "application/json", "teste":"Teste"}
    conteudo = [
        {"aluno": "daniel"},
        {"aluno": "joao"}
    ]
    return make_response(json.dumps(conteudo), 404, headers)