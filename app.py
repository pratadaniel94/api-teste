from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/<string:nome>', methods=["GET"])
def index(nome):
    return jsonify({'nome':nome})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
