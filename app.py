import os
import utils

from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/contact-us', methods=('GET', 'POST'))
def contact_us():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            if not name:
                error = 'Debes ingresar tu nombre'
                flash(error)
                return render_template('contact-us.html')

            if not email:
                error = 'Debes ingresar tu email'
                flash(error)
                return render_template('contact-us.html')

            if not message:
                error = 'Debes ingresar tu mensaje'
                flash(error)
                return render_template('contact-us.html')

        return render_template('contact-us.html')
    except Exception as ex:
        print(ex)
        return render_template('contact-us.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            if not email:
                error = 'Debes ingresar un email'
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')

            if email == 'prueba@gmail.com' and password == 'Prueba123':  # Codigo de prueba login
                # return redirect('mensaje')  # Codigo de prueba login
                return redirect(url_for('dashboard'))
            else:
                error = 'Email o contraseña inválidos.'
                flash(error)
                return render_template('login.html')

        return render_template('login.html')
    except Exception as ex:
        print(ex)
        return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':

            password = request.form['password']
            email = request.form['email']

            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isPasswordValid(password):
                error = "El password no es valido"
                flash(error)
                return render_template('register.html')

        return render_template('register.html')
    except Exception as e:
        print(e)
        return render_template('register.html')


@app.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    try:
        if request.method == 'POST':
            email = request.form['email']
            if not email:
                error = 'Debes ingresar un email'
                flash(error)
                return render_template('forgot-password.html')

        return render_template('forgot-password.html')
    except Exception as e:
        print(e)
        return render_template('forgot-password.html')


@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    return render_template('dashboard.html')


@app.route('/doctors', methods=('GET', 'POST'))
def doctors():
    return render_template('doctors.html')


@app.route('/patients', methods=('GET', 'POST'))
def patients():
    return render_template('patients.html')


@app.route('/appointments', methods=('GET', 'POST'))
def appointments():
    return render_template('appointments.html')


if __name__ == '__main__':
    app.run()
