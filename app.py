import functools
import os
import utils

from db import get_db

from flask import Flask, render_template, flash, request, redirect, url_for, session, g, make_response
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
                    session.clear()
                    session['user_id'] = user[0]
                    resp = make_response(redirect(url_for('profile')))
                    resp.set_cookie('username', email)
                    return resp
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
        print(f'Ha ocurrido el siguiente error: {e}')
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


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


@app.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    try:
        db = get_db()
        doctor = db.execute('SELECT count(role) FROM users where role = 2').fetchone()[0]
        db.commit()

        db = get_db()
        patient = db.execute('SELECT count(role) FROM users where role = 3').fetchone()[0]
        db.commit()

        db = get_db()
        appointment = db.execute('SELECT count(id) FROM appointments where status = 2').fetchone()[0]
        db.commit()

        db = get_db()
        avg = db.execute('SELECT AVG(rate) FROM appointments').fetchone()[0]
        db.commit()

        return render_template('dashboard.html', doctor=doctor, patient=patient, appointment=appointment, avg=avg)
    except Exception as e:
        print(e)
        return render_template('dashboard.html')


@app.route('/doctors', methods=('GET', 'POST'))
@login_required
def doctors():
    return render_template('doctors.html')


@app.route('/patients', methods=('GET', 'POST'))
@login_required
def patients():
    return render_template('patients.html')


@app.route('/appointments', methods=('GET', 'POST'))
@login_required
def appointments():
    return render_template('appointments.html')


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


@app.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    return render_template('profile.html')


@app.route('/all-users')
@login_required
def all_users():
    db = get_db()
    users = db.execute(
        'SELECT id, first_name, last_name, document_type, document_number, role, status  FROM users').fetchall()
    users = list(users)

    # Por corregir
    for user in users:
        for d in user:
            if user.index(d) == 5:
                print(d)
    return render_template('/users/all-users.html', users=users)


@app.route('/create-user', methods=('GET', 'POST'))
@login_required
def create_user():
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
            role = request.form['role']

            """Asignamos 1 como estado por defecto. Este representa el estado Activo """
            status = 1

            # Validaciones
            if not utils.isNameValid(first_name):
                error = "El nombre no es válido"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isNameValid(last_name):
                error = "El apellido no es válido"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isPhone_numberValid(phone):
                error = "El número de telefono no es válido"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isId_NumberValid(document_number):
                error = "El número de documento no es válido"
                flash(error)
                return render_template('/users/create-user.html')

            if gender == "":
                error = "Debe seleccionar un género"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isAddressValid(address):
                error = "La dirección no es válida"
                flash(error)
                return render_template('/users/create-user.html')

            if not utils.isPasswordValid(password):
                error = "La contraseña debe tener al menos 8 dígitos y tener un número, una mayúscula y un caracter especial"
                flash(error)
                return render_template('/users/create-user.html')

            db = get_db()
            db.execute(
                "INSERT INTO users (first_name, last_name, email, phone, document_type, document_number, gender, address, password, role, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, phone, document_type, document_number, gender, address,
                 generate_password_hash(password), role, status))
            db.commit()
            flash("Registro exitoso", "success")
            return redirect(url_for('all_users'))

        return render_template('/users/create-user.html')
    except Exception as e:
        print(f'Ha ocurrido el siguiente error: {e}')
        return redirect(url_for('create_user'))
    return render_template('/users/create-user.html')


@app.route('/users/<id>', methods=('GET', 'POST'))
@login_required
def get_user(id):
    try:
        if request.method == 'GET':
            db = get_db()
            user = db.execute(
                'SELECT id, first_name, last_name, email, phone, document_type, document_number, gender, address, role, status FROM users WHERE id = ?',
                (id,)).fetchone()

            if user:
                return render_template('/users/user-profile.html', user=user)

            flash("No se encontro el usuario con id " + id, "danger")

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            document_type = request.form['document_type']
            document_number = request.form['document_number']
            gender = request.form['gender']
            address = request.form['address']
            role = request.form['role']
            status = request.form['status']

            # Agregar validaciones

            db = get_db()
            db.execute(
                'UPDATE users SET first_name = ?, last_name = ?, email = ?, phone = ?, document_type = ?, document_number = ?, gender = ?, address = ?, role = ?, status = ? WHERE id = ?',
                (first_name, last_name, email, phone, document_type, document_number, gender, address, role, status,
                 id))
            db.commit()
            flash('Se actualizaron los datos correctamente', "success")
    except Exception as e:
        flash(f'Ha ocurrido el siguiente error: {e}', "danger")
        return redirect(url_for('all_users'))

    return redirect(url_for('all_users'))


@app.route('/delete-user/<id>', methods=['POST'])
def delete_user(id):
    try:
        db = get_db()
        db.execute(
            'DELETE FROM users WHERE id = ?', (id,))
        db.commit()
        flash('Se ha eliminado el usuario de la base de datos', "success")

    except Exception as e:
        flash(f'Ha ocurrido el siguiente error: {e}', "danger")
        return redirect(url_for('all_users'))

    return redirect(url_for('all_users'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))
