from flask import Flask, render_template, redirect, url_for, session, flash, request  # Asegúrate de incluir 'request'
from db_connection import create_connection  # Asegúrate de que este archivo exista
from modulos.gestiones import gestiones_bp
from modulos.logistica import logistica_bp
from modulos.configuración import configuración_bp
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para sesiones y mensajes flash

# Registrar los blueprints de cada módulo
app.register_blueprint(gestiones_bp)
app.register_blueprint(logistica_bp)
app.register_blueprint(configuración_bp)

# Ruta de inicio de sesión
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    # Establece la conexión
    connection = create_connection()
    if connection is None:
        flash("Error al conectar a la base de datos.", "error")
        return render_template('login.html')

    cursor = connection.cursor(dictionary=True)  # Usando el cursor con diccionario
    cursor.execute("SELECT * FROM credenciales WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        # Ahora puedes acceder con el nombre de la columna
        session['username'] = result['username']
        return redirect(url_for('menu'))
    else:
        flash("Contraseña incorrecta.", "error")
        return render_template('login.html')

# Ruta para el menú principal
@app.route('/menu')
def menu():
    username = session.get('username')
    if username:
        return render_template('menu.html', username=username)
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
