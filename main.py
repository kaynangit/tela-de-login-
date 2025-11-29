# iportações falsk com falsklogin
from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Usuario
from flask_login import LoginManager, login_user, login_required


# faz a inicialização do falsk e define uma chave secrata para o banco de dados que deveria está no .env(mas está aqui por questões didáticas)
app = Flask(__name__)
app.secret_key = 'teste'
lm = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

'''usa o login maneger para manter o usuario logado caso já tenha feito login anteriormente'''
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id = id).first()
    return usuario


'''redireciona o usuario para a pagina de login realizado com sucesso e usa o login required para só permitir o acesso
caso o usuario já tenha sido logado '''
@app.route('/')
@login_required
def poslogin():
    return render_template('poslogin.html')

'''cria uma rota para a pagina de login que tanto recebe os dados de novos usuario e registra no banco de dados quanto 
redireciona usuarios já cadastrados'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
       return render_template('front.html')
    elif request.method == 'POST':
        
        nome = request.form['nome']
        senha = request.form['senha']

        novo_usuario = Usuario(nome = nome, senha = senha)
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        return redirect(url_for('poslogin'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)


