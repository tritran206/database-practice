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

    def __init__(self, name):
        self.name = name


@app.route('/', methods=['POST', 'GET'])
def todos():

    if request.method == 'POST':
        task = request.form['task']
        new_task = Tasks(task)
        db.session.add(new_task)
        db.session.commit()

    tasks = Tasks.query.all()

    return render_template('todos.html', title="Task-List", tasks=tasks)

@app.route('/delete-task', methods=['POST'])
def remove_task():
    task_id = int(request.form['task-id'])
    task = Tasks.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run()
