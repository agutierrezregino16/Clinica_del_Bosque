import os
import utils

from db import get_db

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

            db = get_db()
            email = db.execute('SELECT * FROM users WHERE email= ? AND password= ?',
                               (email, password)).fetchone()

            if email is None:
                error = 'Correo o contraseña inválidos'
                flash(error)
            else:
                return redirect('dashboard')

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
            name = request.form['name']
            id_type = request.form['id_type']
            id_number = request.form['id_number']
            sex = request.form['sex']
            birth_date = request.form['birth_date']
            address = request.form['address']
            city = request.form['city']
            phone_number = request.form['phone_number']

            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isPasswordValid(password):
                error = "El password no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isNameValid(name):
                error = "Su nombre no es válido"
                flash(error)
                return render_template('register.html')

            if id_type == "":
                error = "Debe seleccionar un tipo de documento"
                flash(error)
                return render_template('register.html')

            if not utils.isId_NumberValid(id_number):
                error = "Su número de documento no es válido"
                flash(error)
                return render_template('register.html')

            if sex == "":
                error = "Debe seleccionar un sexo"
                flash(error)
                return render_template('register.html')

            if birth_date == "":
                error = "Debe ingresar su fecha de nacimiento"
                flash(error)
                return render_template('register.html')

            if not utils.isAddressValid(address):
                error = "Su dirección no es válida"
                flash(error)
                return render_template('register.html')

            if not utils.isNameValid(city):
                error = "Debe ingresar su ciudad"
                flash(error)
                return render_template('register.html')

            if not utils.isPhone_numberValid(phone_number):
                error = "Su número de telefono no es válido"
                flash(error)
                return render_template('register.html')

            db = get_db()
            db.execute(
                "INSERT INTO users (email, password, name, id_type, id_number, sex, birth_date, address, city, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (email, password, name, id_type, id_number, sex, birth_date, address, city, phone_number))
            db.commit()

            return redirect(url_for('login'))

        return render_template('register.html')
    except Exception as e:
        print('2')
        print(e)
        return redirect(url_for('login'))


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
