from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://task-list:password@localhost:8889/task-list'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'secret'
db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes  and 'email' not in session:
        return redirect ('/login')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        email_error = ''
        password_error = ''
        verify_error = ''

################## Validating password
        if password == '':
            password_error = 'Please enter a valid password'
            password = ''
            verify = ''

        elif ' ' in password:
            password_error = 'Password can not contain spaces'
            password = ''
            verify = ''

        elif len(password) <= 3:
            password_error = 'Your password is not long enough'
            password = ''
            verify = ''

        elif len(password) > 20:
            password_error = 'Your password is too long'
            password = ''
            verify = ''

        elif password != verify:
            verify_error = 'Passwords did not match.'
            password = ''
            verify = ''

################## Validating email
        if email:
            if "@" not in email:
                email_error = 'Your email is invalid'
            if "." not in email:
                email_error = 'Your email is invalid'
            if " " in email:
                email_error = 'Your email is invalid'

        if not password_error and not verify_error and not email_error:
            existing_user = User.query.filter_by(email=email).first()
            if not existing_user:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/')
            else:
                email_error = 'This email has already been registered'
                return render_template('register.html', email_error=email_error)

        else:
            return render_template('register.html', email_error=email_error, password_error=password_error, verify_error=verify_error)
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/')
        else:
            error = 'Login failed'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

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
