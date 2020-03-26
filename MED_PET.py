from flask import Flask, request, render_template
from contextlib import closing
import sqlite3
from twitter import tweets 

app = Flask(__name__)

###########################
##  Nossas Rotas e suas  ##
##  funcionalidades      ##
###########################

@app.route("/")
def menu():
    return render_template("menu.html", mensagem = "")

@app.route("/medicamento")
def listar_medicamentos_api():
    return render_template("lista_medicamentos.html", medicamentos = listar_medicamentos())

@app.route("/medicamento/novo", methods = ["GET"])
def form_criar_medicamento_api():
    return render_template("form_medicamento.html", id_medicamento = "novo", nome = "", descricao = "", dosagem = "", indicacao = "", porte = "", composicao = "", marca = "")

@app.route("/medicamento/novo", methods = ["POST"])
def criar_medicamento_api():
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    dosagem = request.form['dosagem']
    indicacao = request.form['indicacao']
    porte = request.form['porte']
    composicao = request.form['composicao']
    marca = request.form['marca']
    id_medicamento = criar_medicamento(nome, descricao, dosagem, indicacao, porte, composicao, marca)
    return render_template("menu.html", mensagem = f"O medicamento {nome} foi criado.")

@app.route("/medicamento/<int:id_medicamento>", methods = ["GET"])
def form_alterar_medicamento_api(id_medicamento):
    medicamento = consultar_medicamento(id_medicamento)
    if medicamento == None:
        return render_template("menu.html", mensagem = f"Esse medicamento não existe."), 404
    return render_template("form_medicamento.html", id_medicamento = id_medicamento, nome = medicamento['nome'], descricao = medicamento['descricao'], dosagem = medicamento['dosagem'], indicacao = medicamento['indicacao'], porte = medicamento['porte'], composicao = medicamento['composicao'], marca = medicamento['marca'])

@app.route("/medicamento/<int:id_medicamento>", methods = ["POST"])
def alterar_medicamento_api(id_medicamento):
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    dosagem = request.form['dosagem']
    indicacao = request.form['indicacao']
    porte = request.form['porte']
    composicao = request.form['composicao']
    marca = request.form['marca']
    medicamento = consultar_medicamento(id_medicamento)
    if medicamento == None:
        return render_template("menu.html", mensagem = f"Esse medicamento não existe."), 404
    editar_medicamento(id_medicamento, nome, descricao, dosagem, indicacao, porte, composicao, marca)
    return render_template("menu.html", mensagem = f"O medicamento {nome} foi alterado.")

@app.route("/medicamento/deletar/<int:id_medicamento>", methods = ["GET"])
def deletar_medicamento_api(id_medicamento):
    medicamento = consultar_medicamento(id_medicamento)
    if medicamento == None:
        return render_template("menu.html", mensagem = f"Esse medicamento não existe."), 404
    deletar_medicamento(id_medicamento)
    return render_template("menu.html", mensagem = f"Medicamento deletado.")

@app.route("/usuario/novo", methods = ["GET"])
def form_criar_usuario_api():
    return render_template("form_usuario.html", id_usuario = "novo", nome_usuario = "", usuario = "", senha = "")

@app.route("/usuario/novo", methods = ["POST"])
def criar_usuario_api():
    nome_usuario = request.form["nome_usuario"]
    usuario = request.form["usuario"]
    senha = request.form['senha']
    id_usuario = criar_usuario(nome_usuario, usuario, senha)
    return render_template("menu.html", mensagem = f"Conta do usuário {nome_usuario} criada com sucesso.")

@app.route("/usuario")
def listar_usuarios_api():
    return render_template("lista_usuarios.html", usuarios = listar_usuarios())

@app.route("/usuario/<int:id_usuario>", methods = ["GET"])
def form_alterar_usuario_api(id_usuario):
    usuario = consultar_usuario(id_usuario)
    if usuario == None:
        return render_template("menu.html", mensagem = f"Esse usuário não existe."), 404
    return render_template("form_usuario.html", id_usuario = id_usuario, nome_usuario = usuario['nome_usuario'], usuario = usuario['usuario'], senha = usuario['senha'])

@app.route("/usuario/<int:id_usuario>", methods = ["POST"])
def alterar_usuario_api(id_usuario):
    nome_usuario = request.form["nome_usuario"]
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    cons_usuario = consultar_usuario(id_usuario)
    if cons_usuario == None:
        return render_template("menu.html", mensagem = f"Esse usuário não existe."), 404
    editar_usuario(id_usuario, nome_usuario, usuario, senha)
    return render_template("menu.html", mensagem = f"O usuário {nome_usuario} foi alterado.")

@app.route("/usuario/deletar/<int:id_usuario>", methods = ["GET"])
def deletar_usuario_api(id_usuario):
    usuario = consultar_usuario(id_usuario)
    if usuario == None:
        return render_template("menu.html", mensagem = f"Esse usuário não existe."), 404
    deletar_usuario(id_usuario)
    return render_template("menu.html", mensagem = f"Usuário deletado.")

@app.route("/login", methods = ["GET"])
def form_login():
    return render_template("login.html", usuario = "", senha = "")

@app.route("/pedido/novo", methods = ["GET"])
def form_insere_produto():
    return render_template("form_insere_produto.html", id_pedido = "novo", usuarios = listar_usuarios(), medicamentos = listar_medicamentos(), qtde_produto = "")

@app.route("/pedido/novo", methods = ["POST"])
def criar_pedido_api():
    nome_usuario = request.form["nome_usuario"]
    nome_produto = request.form["nome_produto"]
    qtde_produto = request.form['qtde_produto']
    id_pedido = criar_pedido(nome_usuario, nome_produto, qtde_produto)
    return render_template("menu.html", mensagem = f"Pedido do usuário {nome_usuario} criado com sucesso.")

@app.route("/pedido")
def listar_pedidos_api():
    return render_template("lista_pedidos.html", pedidos = listar_pedidos())

@app.route("/pedido/<int:id_pedido>", methods = ["GET"])
def form_alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    return render_template("form_insere_produto.html", id_pedido = id_pedido, usuarios = listar_usuarios(), medicamentos = listar_medicamentos(), qtde_produto = pedido['qtde_produto'])

@app.route("/twitter")
def listar_tweets_api():
    listados = listar_tweets()
    return render_template("twitter.html", tweets = listados)

@app.route("/pedido/<int:id_pedido>", methods = ["POST"])
def alterar_pedido_api(id_pedido):
    nome_usuario = request.form["nome_usuario"]
    nome_produto = request.form["nome_produto"]
    qtde_produto = request.form['qtde_produto']
    cons_pedido = consultar_pedido(id_pedido)
    if cons_pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    editar_pedido(id_pedido, nome_usuario, nome_produto, qtde_produto)
    return render_template("menu.html", mensagem = f"O pedido do Usuário {nome_usuario} foi alterado.")

#############################
##  Tratativas Dicionários ##
#############################

def row_to_dict(description, row):
    if row == None:
        return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

###########################
##  Criação das Tabelas  ##
##  do Banco de Dados    ##
###########################

sql_create = """
CREATE TABLE IF NOT EXISTS medicamento (
    id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    descricao VARCHAR(500) NULL,
    dosagem VARCHAR(500) NULL,
    indicacao VARCHAR(500) NULL,
    porte VARCHAR(200) NULL,
    composicao VARCHAR(500) NOT NULL,
    marca VARCHAR(120) NOT NULL
);
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario VARCHAR(200) NOT NULL,
    usuario VARCHAR(120) NOT NULL,
    senha VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario VARCHAR(200) NOT NULL,
    nome_produto VARCHAR(200) NOT NULL,
    qtde_produto INTEGER(10) NOT NULL
);
"""
############################
## Funções que interferem ##
## diretamente no banco   ##
############################

def conectar():
    return sqlite3.connect('med_pet.db')

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()

def listar_medicamentos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_medicamento, nome, descricao, dosagem, indicacao, porte, composicao, marca FROM medicamento ORDER BY id_medicamento")
        return rows_to_dict(cur.description, cur.fetchall())

def listar_medicamentos_ordem():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_medicamento, nome, descricao, dosagem, indicacao, porte, composicao, marca FROM medicamento ORDER BY nome")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_medicamento(id_medicamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_medicamento, nome, descricao, dosagem, indicacao, porte, composicao, marca FROM medicamento WHERE id_medicamento = ?", (id_medicamento, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_medicamento(nome, descricao, dosagem, indicacao, porte, composicao, marca):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO medicamento (nome, descricao, dosagem, indicacao, porte, composicao, marca) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, descricao, dosagem, indicacao, porte, composicao, marca))
        id_medicamento = cur.lastrowid
        con.commit()
        return id_medicamento

def editar_medicamento(id_medicamento, nome, descricao, dosagem, indicacao, porte, composicao, marca):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE medicamento SET nome = ?, descricao = ?, dosagem = ?, indicacao = ?, porte = ?, composicao = ?, marca = ? WHERE id_medicamento = ?", (nome, descricao, dosagem, indicacao, porte, composicao, marca, id_medicamento))
        con.commit()

def deletar_medicamento(id_medicamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM medicamento WHERE id_medicamento = ?", (id_medicamento,))
        con.commit()

def criar_usuario(nome_usuario, usuario, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuario (nome_usuario, usuario, senha) VALUES (?, ?, ?)", (nome_usuario, usuario, senha))
        id_usuario = cur.lastrowid
        con.commit()
        return id_usuario

def listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_usuario, nome_usuario, usuario, senha FROM usuario ORDER BY id_usuario")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_usuario(id_usuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_usuario, nome_usuario, usuario, senha FROM usuario WHERE id_usuario = ?" , (id_usuario, ))
        return row_to_dict(cur.description, cur.fetchone())

def editar_usuario(id_usuario, nome_usuario, usuario, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE usuario SET nome_usuario = ?, usuario = ?, senha = ? WHERE id_usuario = ?", (nome_usuario, usuario, senha, id_usuario))
        con.commit()

def deletar_usuario(id_usuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        con.commit()

def criar_pedido(nome_usuario, nome_produto, qtde_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO pedido (nome_usuario, nome_produto, qtde_produto) VALUES (?, ?, ?)", (nome_usuario, nome_produto, qtde_produto))
        id_pedido = cur.lastrowid
        con.commit()
        return id_pedido

def listar_pedidos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_pedido, nome_usuario, nome_produto, qtde_produto FROM pedido ORDER BY id_pedido")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_pedido, nome_usuario, nome_produto, qtde_produto FROM pedido WHERE id_pedido = ?" , (id_pedido, ))
        return row_to_dict(cur.description, cur.fetchone())

def editar_pedido(id_pedido, nome_usuario, nome_produto, qtde_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE pedido SET nome_usuario = ?, nome_produto = ?, qtde_produto = ? WHERE id_pedido = ?", (nome_usuario, nome_produto, qtde_produto, id_pedido))
        con.commit()

def listar_tweets():
        df = tweets()
        return df

if __name__ == "__main__":
    criar_bd()
    app.run(port = 8000, debug = True)