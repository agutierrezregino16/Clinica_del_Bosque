import os
import utils

from db import get_db

from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

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
                flash(error, "danger")
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error, "danger")
                return render_template('login.html')

            db = get_db()
            user = db.execute('SELECT * FROM users WHERE email= ?', (email,)).fetchone()

            if user is None:
                error = 'El usuario no existe'
            else:
                store_password = user[9]
                result = check_password_hash(store_password, password)
                if result is False:
                    error = 'Usuario o contraseña inválidos'
                else:
                    return redirect('dashboard')
            flash(error, "danger")

        return render_template('login.html')
    except Exception as ex:
        print(ex)
        return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            document_type = request.form['document_type']
            document_number = request.form['document_number']
            gender = request.form['gender']
            address = request.form['address']
            password = request.form['password']

            """"Asignamos el rol 3 automáticamente, este es el rol paciente.
            Todos los usuarios que se registren por este formulario serán asignados como pacientes"""
            role = 3

            """Asignamos 1 como estado por defecto. Este representa el estado Activo """
            status = 1

            # Validaciones
            if not utils.isNameValid(first_name):
                error = "El nombre no es válido"
                flash(error)
                return render_template('register.html')

            if not utils.isNameValid(last_name):
                error = "El apellido no es válido"
                flash(error)
                return render_template('register.html')

            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isPhone_numberValid(phone):
                error = "El número de telefono no es válido"
                flash(error)
                return render_template('register.html')

            if document_type == "":
                error = "Debe seleccionar un tipo de documento"
                flash(error)
                return render_template('register.html')

            if not utils.isId_NumberValid(document_number):
                error = "El número de documento no es válido"
                flash(error)
                return render_template('register.html')

            if gender == "":
                error = "Debe seleccionar un género"
                flash(error)
                return render_template('register.html')

            if not utils.isAddressValid(address):
                error = "La dirección no es válida"
                flash(error)
                return render_template('register.html')

            if not utils.isPasswordValid(password):
                error = "La contraseña debe tener al menos 8 dígitos y tener un número, una mayúscula y un caracter especial"
                flash(error)
                return render_template('register.html')

            db = get_db()
            db.execute(
                "INSERT INTO users (first_name, last_name, email, phone, document_type, document_number, gender, address, password, role, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, phone, document_type, document_number, gender, address,
                 generate_password_hash(password), role, status))
            db.commit()
            flash("Registro exitoso, por favor inicie sesión", "success")
            return redirect(url_for('login'))

        return render_template('register.html')
    except Exception as e:
        print(f'Ha ocurrido el siguitente error: {e}')
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
