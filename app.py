import os

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Inicio.html')
def inicio():
    return render_template('Inicio.html')


@app.route('/Quienes-somos.html')
def acerca_de():
    return render_template('Quienes-somos.html')


@app.route('/Contacto.html')
def contact():
    return render_template('Contacto.html')


@app.route('/Iniciar-sesión.html')
def login():
    return render_template('Iniciar-sesión.html')


@app.route('/Registrarse.html')
def registro():
    return render_template('Registrarse.html')


@app.route('/Olvido-la-contraseña.html')
def forgot_password():
    return render_template('Olvido-la-contraseña.html')


if __name__ == '__main__':
    app.run()
