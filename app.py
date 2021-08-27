import sqlite3
from flask import Flask, request, url_for, session, g, redirect, abort, render_template, flash

# configuração
DATABASE = "blog.db"
SECRET_KEY = "pudim"

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def depois_request(exc):
    g.bd.close()

@app.route('/')
@app.route('/entradas')
def exibir_entradas():
    #return "<h1>Aqui estarão as postagens!!</h1>"
    #return render_template('exibir_entradas.html', mensagem="Olá pessoas!", img="https://image.freepik.com/fotos-gratis/imagem-aproximada-em-tons-de-cinza-de-uma-aguia-careca-americana-em-um-fundo-escuro_181624-31795.jpg")
    sql = "SELECT titulo, texto FROM entradas order by id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall():
        entradas.append({'titulo': titulo, 'texto': texto})
    return render_template('exibir_entradas.html', entradas=entradas)

#@app.route('/hello')
#def pagina_inicial():
#    return "Hello World"

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?,?)"
    g.bd.execute(sql, (request.form['campoTitulo'], request.form['campoTexto']))
    g.bd.commit()
    #sql = "INSERT INTO entradas(titulo, texto) VALUES ('Segundo Post','Esse é o segundo post')"
    #g.bd.execute(sql)
    #g.bd.commit()
    return redirect('/entradas')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('exibir_entradas'))

@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form['campoUsuario'] != 'admin' \
            and request.form['campoSenha'] != 'admin':
            erro = "Senha ou Usuário Inválidos"
        else:
            session['logado'] = True
            return redirect(url_for('exibir_entradas'))

    return render_template('login.html', erro=erro)