from flask import Flask, render_template, request
from requests import api
from acessoBD import insert, select


def cepException(dic, resposta):
    if resposta.status_code == 400:
        dic["cep"] = "Not Found!"
        dic["logradouro"] = "Not Found!"
        return 1
    return 0


def inputDados(dic, where, content):
    dic[where] = content
    return dic


app = Flask("__name__")

user = {
    "ra": "",
    "nome": "",
    "senha": "",
    "email": "",
    "cep": "",
    "endereco": "",
    "bairro": "",
    "numero": ""
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    ra = request.form["ra"]
    nome = request.form["nome"]
    senha = request.form["senha"]
    email = request.form["email"]
    cep = request.form["cep"]
    numero = request.form["numero"]

    resposta = api.get(f"https://viacep.com.br/ws/{cep}/json/")
    validacao = cepException(user, resposta)

    if validacao == 0:
        endereco = resposta.json()["logradouro"]
        bairro = resposta.json()["bairro"]
        inputDados(user, "ra", ra)
        inputDados(user, "nome", nome)
        inputDados(user, "senha", senha)
        inputDados(user, "email", email)
        inputDados(user, "cep", cep)
        inputDados(user, "endereco", endereco)
        inputDados(user, "bairro", bairro)
        inputDados(user, "numero", numero)
    else:
        inputDados(user, "ra", ra)
        inputDados(user, "nome", nome)
        inputDados(user, "senha", senha)
        inputDados(user, "email", email)
        inputDados(user, "cep", cep)
        inputDados(user, "numero", numero)

    insert(user)

    return render_template("sucessful.html")


@app.route("/logar", methods=["POST"])
def logar():
    ra = request.form['ra']
    senha = request.form['senha']
    return_bd = select(ra)
    if ra == return_bd[0]:
        if senha == return_bd[1]:
            return print("Sucesso!")
        else:
            return print("RA ou Senha errada!")
    else:
        return print("RA ou Senha errada!")


@app.route("/encaminhar", methods=["POST"])
def encaminhar():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
