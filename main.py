from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://task-list:password@localhost:8889/task-list'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

@app.route('/', methods=['POST', 'GET'])
def todos():

    if request.method == 'POST':
        task = request.form['task']
        new_task = Tasks(task)
        db.session.add(new_task)
        db.session.commit()

    tasks = Tasks.query.filter_by(completed=False).all()
    completed_tasks = Tasks.query.filter_by(completed=True).all()

    return render_template('todos.html', title="Task-List", tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def remove_task():
    task_id = int(request.form['task-id'])
    task = Tasks.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run()
