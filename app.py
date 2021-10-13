import os
import utils

from flask import Flask, render_template, flash, request, redirect, jsonify

from message import mensajes

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/contact-us')
def contact_us():
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
                return render_template('dashboard.html')
            else:
                error = 'Email o contraseña inválidos.'
                flash(error)
                return render_template('login.html')
        return render_template('login.html')
    except Exception as ex:
        print(ex)
        return render_template('login.html')
    return render_template('login.html')


@app.route('/mensaje')  # Codigo de prueba login
def message():  # Codigo de prueba login
    return jsonify({'usuario': mensajes, 'mensaje': 'Mensajes'})


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
    return render_template('register.html')


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
