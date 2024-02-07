from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import cli

from controller import UserController, TodoController
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Flask-Login için gerekli olan gizli anahtar

db.init_app(app)

# Flask-Login yapılandırması
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Giriş yapılması gereken sayfanın adı (örneğin, login.html)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Kullanıcı İşlemleri
app.route('/register', methods=['GET', 'POST'])(UserController.register)
app.route('/login', methods=['GET', 'POST'])(UserController.login)
app.route('/logout')(UserController.logout)

# Todo İşlemleri
app.route('/todos', methods=['GET'])(TodoController.list_todos)
app.route('/todos/add', methods=['GET', 'POST'])(TodoController.add_todo)
app.route('/todos/<int:todo_id>/update', methods=['POST'])(TodoController.update_todo)
app.route('/todos/<int:todo_id>/delete', methods=['POST'])(TodoController.delete_todo)

@app.route('/')
def index():
    return render_template('login.html')

@app.cli.command("create_db")
def create_db():
    db.create_all()

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()

if __name__ == "__main__":
    app.run(debug=True)