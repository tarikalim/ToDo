from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
