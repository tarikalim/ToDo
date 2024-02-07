from flask import request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db, Todo


class UserController:
    @staticmethod
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            # Kullanıcı adı ve e-posta adresi benzersiz olmalıdır
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                return "Kullanıcı adı veya e-posta adresi zaten kullanımda!"
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Kayıt işlemi tamamlandıktan sonra oturum açma sayfasına yönlendir
        return render_template('register.html')

    @staticmethod
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('list_todos'))  # Oturum açma başarılıysa todo listesine yönlendir
            return "Geçersiz kullanıcı adı veya şifre!"
        return render_template('login.html')

    @staticmethod
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))  # Oturum kapatıldıktan sonra ana sayfaya yönlendir


class TodoController:
    @staticmethod
    @login_required
    def list_todos():
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template('todos.html', todos=todos)

    @staticmethod
    @login_required
    def add_todo():
        if request.method == 'POST':
            title = request.form.get('title')
            new_todo = Todo(title=title, user_id=current_user.id)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('list_todos'))  # Todo eklendikten sonra todo listesine yönlendir
        return render_template('add_todo.html')

    @staticmethod
    @login_required
    def update_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id == current_user.id:
            todo.complete = not todo.complete
            db.session.commit()
        return redirect(url_for('list_todos'))  # Todo güncellendikten sonra todo listesine yönlendir

    @staticmethod
    @login_required
    def delete_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id == current_user.id:
            db.session.delete(todo)
            db.session.commit()
        return redirect(url_for('list_todos'))  # Todo silindikten sonra todo listesine yönlendir
