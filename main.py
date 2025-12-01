# iportações falsk com falsklogin
from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Usuario
from flask_login import LoginManager, login_user, login_required, logout_user
import hashlib 


# faz a inicialização do falsk e define uma chave secrata para o banco de dados que deveria está no .env(mas está aqui por questões didáticas)
app = Flask(__name__)
app.secret_key = 'teste'
lm = LoginManager(app)
lm.login_view = 'cadastrar'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

'''criptografa a senha e salvano banco de dados'''
def hash(txt):
    hasPass = hashlib.sha256(txt.encode('utf-8'))
    return hasPass.hexdigest()


'''usa o login maneger para manter o usuario logado caso já tenha feito login anteriormente'''
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id = id).first()
    return usuario


'''redireciona o usuario para a pagina de login realizado com sucesso e usa o login required para só permitir o acesso
caso o usuario já tenha sido logado '''

@app.route('/')
@login_required
def home():
    return render_template('home.html')

'''essa rota leva a tela de login para acessar o site e so pode ser acessada caso o usuario já tenha feito cadastro, 
porem se o nome ou senha estiverem errados emite um aviso  '''
@app.route('/criar', methods = ['GET', 'POST'])
def criar():
    if request.method == "GET":
        return render_template('criar_conta.html')
    elif request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        user = db.session.query(Usuario).filter_by(nome = nome, senha = hash(senha)).first()
        if not user:
            return  'Nome ou senha incorretos'
        
        login_user(user)
        return redirect(url_for('home'))

'''cria uma rota para a pagina de login que tanto recebe os dados de novos usuario e registra no banco de dados quanto 
redireciona usuarios já cadastrados'''

@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
       return render_template('cadastrar.html')
    elif request.method == 'POST':
        
        nome = request.form['nome']
        senha = request.form['senha']

        novo_usuario = Usuario(nome = nome, senha = hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        return redirect(url_for('criar'))

'''Rota de logout para caso o usuario queira sair do site'''
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('criar'))
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
