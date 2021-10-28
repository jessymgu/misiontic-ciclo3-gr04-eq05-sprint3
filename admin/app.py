import os
from types import MethodDescriptorType
from flask import Flask, render_template, flash, url_for, request, session,redirect
import yagmail as yagmail
import utils
from forms import FormInicio
import sqlite3
from sqlite3 import Error
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__) # __name__ busca archivos estáticos
app.secret_key = os.urandom(24)

url_for.__init__
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/superadmin-dashboard', methods=["GET"])
def superadmin_index():
    return render_template('index.html')
    # !El dashboard únicamente muestra la información consignada en la BD. Desde el navegador no se envía información al servidor. Por lo tanto, usa exclusivamente el método "GET"

@app.route('/superadmin-pacientes', methods=["GET", "POST"])
def superadmin_pacientes():
    return render_template('patients.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página pacientes)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear (registrar) un nuevo paciente, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)

@app.route('/superadmin-medicos', methods=["GET", "POST"])
def superadmin_medicos():
    return render_template('doctors.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página medicos)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear (registrar) un nuevo médico, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)

@app.route('/superadmin-citas', methods=["GET", "POST"])
def superadmin_citas():
    return render_template('appointments.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página citas)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear una nueva cita, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)

@app.route('/route_name')
def method_name():
    pass



# Inicio Rutas - AndrésCC
@app.route("/login", methods=["GET" , "POST"])
def login():
    form = FormInicio()
    if (form.validate_on_submit()):
        flash(f"Inicio de sesión solicitada por el usuario {form.username.data}")
        # return redirect(url_for("login_init"))
    # return render_template("login.html", form=form) 
        #base de datos
        if request.method == 'POST':
            user = escape(request.form['username'])
            password = escape(request.form['password'])

            try:
                with sqlite3.connect("DB_Clinica_RC_Users.db") as con:
                    cur = con.cursor()
                    query = cur.execute("SELECT Contraseña FROM Usuarios WHERE Nombre_usuario=?", [user]).fetchone()
                    if query != None:
                        if check_password_hash(query[0], password):
                            session['user'] = user
                            return redirect("/login_correcto")  # Redireccionar a otra ruta
                            # return rendert_template("home.html") #Renderiza la vista pero no te cambia la ruta
                        else:
                            return "Credenciales incorrectas"
                    else:
                        return "El usuario NO existe"
            except Error:
                print(Error)

        if 'user' in session:
            return redirect('/login_correcto')
        else:
            return render_template("login.html, form=form")
        
    else:
        return render_template("login.html", form=form)


""" @app.route("/login_correcto")
def login_init():
    return render_template("login_correcto.html") """


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = escape(request.form['name'])
        apell= escape(request.form['apell'])
        docum= escape(request.form['docum'])
        gen = escape(request.form['gen'])
        email = escape(request.form['email'])
        fecha_nac= escape(request.form['fecha_nac'])
        resid = escape(request.form['resid'])
        ciudad= escape(request.form['ciu'])
        tel = escape(request.form['tel'])
        user = escape(request.form['username'])
        tipo_user = escape(request.form['tipo_user'])
        pass_1 = escape(request.form['pass1'])
        pass_2 = escape(request.form['pass2'])

        
        if pass_1 != pass_2:
            return "Las contraseñas no coinciden"
        else:
            hash_clave = generate_password_hash(pass_1)
            try:
                with sqlite3.connect("DB_Clinica_RC_Users.db") as con:
                    cur = con.cursor()

                    existe = cur.execute(
                        "SELECT Nombre_usuario FROM Usuarios WHERE Nombre_usuario=?", [user]).fetchone()

                    if existe!= None:
                        return "El Usuario ya existe, por favor intente de nuevo"
                    else:             
                        cur.execute("INSERT INTO Usuarios(Nombre,Apellido, Documento, Fecha_nac, Genero, Email, Residencia, Ciudad, Telefono, Tipo_usuario, Nombre_usuario,Contraseña) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                           name, apell, docum, fecha_nac, gen, email, resid, ciudad, tel, tipo_user,  user, hash_clave))
                        con.commit()
                        return "Guardado con exito"

            except Error:
                print(Error)
                return "Registro no completado"

    return render_template('register.html')

@app.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")


@app.route('/login_correcto', methods=['GET'])
def login_correcto():
    if 'user' in session:
        try:
            with sqlite3.connect("DB_Clinica_RC_Users.db") as con:

                con.row_factory = sqlite3.Row
                cur = con.cursor()
                query = cur.execute("SELECT Tipo_usuario, Nombre, Email, Genero FROM Usuarios WHERE Nombre_usuario=?", [
                                    session['user']]).fetchone()

                if query is None:
                    return("El usuario no existe")

        except Error:
            print(Error)

        return render_template('login_correcto.html', tipo_user=query[0], name=query[1], email=query[2], gen=query[3])
    else:
        return "<a href='/'>Por favor inicie sesión</a>"


@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.clear()
        return redirect('/')
    else:
        return "<a href='/login'>Inicie sesión</a>"

# Fin Rutas - AndrésCC 


if __name__ == '__main__': #activar modo debug
    app.run(debug=True)