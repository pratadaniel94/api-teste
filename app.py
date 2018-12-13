from flask import Flask, jsonify, request
from pymongo import MongoClient
from modulos.alunos import alunos

try:
    con = MongoClient()
    db = con['teste']
except Exception as e:
    print(e)

app = Flask(__name__)
app.register_blueprint(alunos)


def validar_json(json, method="GET"):
    if json:
        try:
            if json['nome'] and json['_id']:
                return True
            else:
                return False
        except KeyError:
            if method == "PUT":
                if json['nome']:
                    return True
            return False
    else:
        return False


@app.route('/usuarios', methods=["GET", "POST"])
def get_or_post_users():
    if request.method == "GET":
        return jsonify(list(db.usuarios.find()))
    else:
        data = request.get_json()
        if isinstance(data, dict):

            if validar_json(data):
                db.usuarios.insert(data)
                return jsonify({"status": True})
            else:
                return jsonify({"status": False})
        elif isinstance(data, list):
            for registro in data:
                if validar_json(registro):
                    db.usuarios.insert(registro)
                else:
                    return jsonify({"status": False})
            else:
                return jsonify({"status": True})


@app.route('/usuarios/<string:busca>', methods=["GET"])
def get_user(busca):
    if busca.isnumeric():
        return jsonify(db.usuarios.find_one({"_id": int(busca)}))
    else:
        return jsonify(list(db.usuarios.find({"nome": busca.lower().strip()})))


@app.route('/usuario/<int:id>', methods=['PUT', 'DELETE'])
def update_user(id):
    if request.method == "PUT":
        data = request.get_json()
        if validar_json(data, method="PUT"):
            db.usuarios.update({"_id":id},{"$set":data})
            return jsonify({"status":True})
        else:
            return jsonify({"status": False})
    elif request.method == "DELETE":
        try:
            db.usuarios.remove({"_id":id})
            return jsonify({"status": True})
        except Exception:
            return jsonify({"status": False})

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
