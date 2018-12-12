from flask import Flask, jsonify, request
from pymongo import MongoClient

try:
    con = MongoClient()
    db = con['teste']
except Exception as e:
    print(e)

app = Flask(__name__)
def validar_json(json):
    if json:
        try:
            if json['nome'] and json['_id']:
                db.usuarios.insert(json)
                return True
            else:
                return False
        except KeyError:
            return False
    else:
        return False


@app.route('/usuarios', methods=["GET", "POST"])
def get_or_post_users():
    if request.method ==  "GET":
        return jsonify(list(db.usuarios.find()))
    else:
        data = request.get_json()
        if isinstance(data, dict):
            status = validar_json(data)
            return jsonify({"status": status})
        elif isinstance(data,list):
            for registro in data:
                if not validar_json(registro):
                    return jsonify({"status": False})

            else:
                return jsonify({"status": True})


# @app.route('/usuarios', methods=['POST' ])
# def register_users():
#     print(request.get_json())
#     print(dir(request))
#     return 'sucess'

@app.route('/usuarios/<string:busca>', methods=["GET"])
def get_user(busca):
    if busca.isnumeric():
        return jsonify(db.usuarios.find_one({"_id": int(busca)}))
    else:
        return jsonify(list(db.usuarios.find({"nome": busca.lower().strip()})))


# @app.route('/<string:nome>', methods=["GET"])
# def index(nome):
    # return jsonify({'nome':nome})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
