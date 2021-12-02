from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash
    )
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(100), nullable=False,unique=True)
    password = db.Column(db.Text(16), nullable=False)
    todos = db.relationship('Todo',backref='owner')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Post(FlaskForm):
    task = StringField("Add a task", validators=[DataRequired()])
    add = SubmitField()


@app.route('/')
def home():
    with open('./README.md', mode='r') as f:
        readme = "".join(l for l in f)
    return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            session['user'] = user.id
            session['logged_in'] = True
            return redirect('/todo/user/1')
        else:
            return redirect('/login')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.get(id)
    if todo:
        return render_template('todo.html', todo=todo)
    else:
        return "<h1>WE cannot find what are you looking for!!<h1>"


@app.route('/todo/user/<pg>', methods=['GET', 'POST'])
@app.route('/todo/user/<pg>', methods=['GET', 'POST'])
def todos(pg):
    form = Post()
    error = None
    if not session.get('logged_in'):
        flash('Invalid credentials', "error")
        return redirect('/login')
    if form.validate_on_submit():
        new_todo = Todo(
            description=form.task.data,
            owner_id=session['user']
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('you added a task', "info")
        return redirect('/todo/user/1')
    else:

        if pg == 1:
            todos = Todo.query.filter_by(owner_id=session['user']).paginate(per_page=10,page=1)
        else:
            todos = Todo.query.filter_by(owner_id=session['user']).paginate(per_page=10,page=int(pg))
        return render_template('todos.html', todos=todos, form=form, error=error)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    post_to_delete = Todo.query.get(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    flash("You deleted a task","info")
    return redirect('/todo/user/1')


@app.route('/todo/<id>/json',methods=['GET'])
def getx(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    if todo is not None:
        dict ={
            "todo_id": todo['id'],
            "user_id": todo['user_id'],
            "description": todo['description']
        }
        return jsonify(dict)
    else:
        dict = {
            "message": "What you are looking for... is not present:|"
        }
        return jsonify(dict)