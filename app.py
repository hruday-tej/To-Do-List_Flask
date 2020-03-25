from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean)



@app.route('/')
def index():
    incomplete = Todo.query.filter_by(completed=False).all()
    complete = Todo.query.filter_by(completed=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], completed=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    # return '<h1>{}</h1>'.format(id)

    todo=Todo.query.filter_by(id=int(id)).first()
    todo.completed = True
    db.session.commit()
    
    return redirect(url_for('index'))




if __name__== '__main__':
    app.run(debug=True)