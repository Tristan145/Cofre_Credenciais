from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Credential
from security import encrypt_string, decrypt_string
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_padrao_mude_depois'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cofre.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configuração de Autenticação
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas de Autenticação
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rotas do Cofre
@app.route('/')
@login_required
def dashboard():
    # Busca apenas as senhas do usuário logado
    credentials = Credential.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', credentials=credentials)

@app.route('/create-credential', methods=['POST'])
@login_required
def create_credential():
    service = request.form.get('service')
    username = request.form.get('username')
    password = request.form.get('password')
    
    new_cred = Credential(
        user_id=current_user.id,
        service=service,
        username=username,
        encrypted_password=encrypt_string(password)
    )
    db.session.add(new_cred)
    db.session.commit()
    flash('Credencial salva com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/revelar_senha/<int:id>', methods=['POST'])
@login_required
def reveal_credential(id):
    credential = Credential.query.get_or_404(id)
    
    if credential.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403

    decrypted_password = decrypt_string(credential.encrypted_password)
    return jsonify({'password': decrypted_password})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria o banco de dados e as tabelas
    app.run(debug=True)