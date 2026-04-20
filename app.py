from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.get('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.post('/tasks')
def create_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    if not title:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template('partials/task_list.html', tasks=tasks, error='Title is required.') , 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    tasks = Task.query.order_by(Task.created_at.desc()).all()
    response = render_template('partials/task_list.html', tasks=tasks)
    return response

@app.get('/tasks/<int:task_id>/edit')
def edit_task_form(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('partials/edit_form.html', task=task)

@app.post('/tasks/<int:task_id>/edit')
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    if not title:
        return render_template('partials/edit_form.html', task=task, error='Title is required.'), 400

    task.title = title
    task.description = description
    db.session.commit()
    return render_template('partials/task_item.html', task=task)

@app.post('/tasks/<int:task_id>/toggle')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return render_template('partials/task_item.html', task=task)

@app.post('/tasks/<int:task_id>/delete')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
