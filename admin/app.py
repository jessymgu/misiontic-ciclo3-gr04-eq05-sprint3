import os
from types import MethodDescriptorType
import sqlite3
from sqlite3 import Error
from flask.helpers import flash
from flask import Flask, render_template, flash, url_for, request, session,redirect
import yagmail as yagmail
import utils
from forms import FormInicio
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
    # return render_template('index.html')
    # !El dashboard únicamente muestra la información consignada en la BD. Desde el navegador no se envía información al servidor. Por lo tanto, usa exclusivamente el método "GET"
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM Pacientes")
            row = cur.fetchall()
            return render_template('index.html',row=row)
    except Error:
        print(Error)


@app.route('/superadmin-pacientes', methods=["GET", "POST"])
def superadmin_pacientes():
    # return render_template('patients.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página pacientes)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear (registrar) un nuevo paciente, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM Pacientes")
            # cur.execute("SELECT * FROM Pacientes")
            row = cur.fetchall()
            return render_template('doctors.html',row=row)
    except Error:
        print(Error)


@app.route('/superadmin-medicos', methods=["GET", "POST"])
def superadmin_medicos():
    # return render_template('doctors.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página medicos)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear (registrar) un nuevo médico, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM Pacientes")
            # cur.execute("SELECT * FROM Medicos")
            row = cur.fetchall()
            return render_template('doctors.html',row=row)
    except Error:
        print(Error)


@app.route('/superadmin-citas', methods=["GET", "POST"])
def superadmin_citas():
#     return render_template('appointments.html')
    # !Primero se usa el método GET para consultar a la información alojada en la BD (vista de la página citas)
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear una nueva cita, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM citaspaciente")
            row = cur.fetchall()
            return render_template('appointments.html',row=row)
    except Error:
        print(Error)


@app.route('/route_name')
def method_name():
    pass

# ----------------------------------------------------------------paciente citas--------------------------------#
@app.route('/citas-paciente', methods=["GET"])
def citaspaciente():
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM citaspaciente")
            row = cur.fetchall()
            return render_template('citaspasiente.html',row=row)
    except Error:
        print(Error)
    # Lista de citas del paciente

@app.route('/detalles-paciente', methods=["GET", "POST"])
def detallespaciente():
    if request.method == 'POST':
        
        id= request.form['Identidad']
        hora= request.form['hora']
        nomdoc= request.form['Nombre_doctor']
        nompac= request.form['Nombre_paciente']
        cita= request.form['cita']
        direc= request.form['Direccion']
        fecha= request.form['fecha']
            
        try:
             with sqlite3.connect('DB_Clinica_RC.db') as con:
                cur = con.cursor()#manipula la conexion
                cur.execute("INSERT INTO citaspaciente (ID,Hora,Nombre_doctor,Nombre_paciente,Tipo,Direccion,Fecha) VALUES (?,?,?,?,?,?,?)",(id,hora,nomdoc,nompac,cita,direc,fecha))
                con.commit()#confirmar los datos enviados o actualiza los cambios en la bd
        except Error:
            print(Error)
            
    return render_template('detallespaciente.html')
    # Detalles de citas del paciente


# ----------------------------------------------------------------medico citas--------------------------------#

@app.route('/citas-medico', methods=["GET"])
def citasmedico():
    try:
        with sqlite3.connect('DB_Clinica_RC.db') as con:
            con.row_factory =sqlite3.Row #convierte la respuesta de la Bd en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM citasmedico")
            row = cur.fetchall()
            return render_template('citasmedico.html',row=row)
    except Error:
        print(Error)
    # Lista de citas del medico

@app.route('/detalles-medico', methods=["GET", "POST"])
def detallesmedico():
    return render_template('detallesmedico.html')
    # Detalles de citas del medico

# -------------------------------------------------vista de los tipos de usuario---------------------------------------------#

@app.route('/detalles-vista-medico', methods=["GET"])
def vista():
    return render_template('vistacita.html')
    # Detalles de citas vista

# -------------------------------------------------resultado de búsqueda---------------------------------------------#
@app.route('/resultados_busqueda', methods=["GET"])
def resultados_busqueda():
    return render_template('resultado.html')


# ------------------------------------------------- perfiles de usuario ---------------------------------------------#
@app.route('/medico-perfil', methods=["GET", "POST"])
def medico_perfil():
    if 'user' in session:
            try:
                with sqlite3.connect("DB_Clinica_RC.db") as con:

                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    query = cur.execute("SELECT Nombre, Email, Genero, Apellido, Telefono,Residencia,Documento, Ciudad FROM Medicos WHERE Nombre_usuario=?", [session['user']]).fetchone()

                    if query is None:
                        flash("El usuario no existe")
                        #return("El usuario no existe")

            except Error:
                print(Error)

            return render_template('perfil_medico.html', name=query[0], email=query[1], gen=query[2], apell=query[3],tel=query[4],resid=query[5],ciu=query[6],docum=query[7])
    return render_template('perfil_medico.html')


@app.route('/paciente-perfil', methods=["GET", "POST"])
def paciente_perfil():
    if 'user' in session:
            try:
                with sqlite3.connect("DB_Clinica_RC.db") as con:

                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    query = cur.execute("SELECT Nombre, Email, Genero, Apellido, Telefono,Residencia,Documento, Ciudad FROM Pacientes WHERE Nombre_usuario=?", [session['user']]).fetchone()

                    if query is None:
                        return("El usuario no existe")

            except Error:
                print(Error)

            return render_template('perfil_paciente.html', name=query[0], email=query[1], gen=query[2], apell=query[3],tel=query[4],resid=query[5],ciu=query[6],docum=query[7])
    return render_template('perfil_paciente.html')



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
            # !tipo_usuario = 

            try:
                with sqlite3.connect("DB_Clinica_RC.db") as con:
                    cur = con.cursor()
                    query = cur.execute("SELECT Contraseña FROM Pacientes WHERE Nombre_usuario=?", [user]).fetchone()
                    if query != None:

                        if check_password_hash(query[0], password):
                            #flash("login correcto")
                            session['user'] = user
                            # !if tipo_usuario == 'paciente':
                            return redirect("/paciente-perfil")  # Redireccionar a otra ruta
                            # return redirect("/login_correcto")  # Redireccionar a otra ruta
                            # return rendert_template("home.html") #Renderiza la vista pero no te cambia la ruta
                        else:
                            flash("credenciales incorrectas")
                            #return "Credenciales incorrectas"
                    else:
                        query2 = cur.execute("SELECT Contraseña FROM Medicos WHERE Nombre_usuario=?", [user]).fetchone()
                        if query2 != None:

                            if check_password_hash(query2[0], password):
                                session['user'] = user
                                return redirect("/medico-perfil")  # Redireccionar a otra ruta    
                            else:
                                flash("credenciales incorrectas")
                                #return "Credenciales incorrectas"

                        else:
                            flash("El usuario no existe en nuestro sistema.")
                            #return "El usuario NO existe"
            except Error:
                print(Error)

        if 'user' in session:
            return redirect('/login_correcto')
        else:
            return render_template("login.html", form=form)
        
    else:
        return render_template("login.html", form=form)


""" @app.route("/login_correcto")
def login_init():
    return render_template("login_correcto.html") """


@app.route('/register_paciente', methods=('GET', 'POST'))
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
        #tipo_user = escape(request.form['tipo_user'])
        pass_1 = escape(request.form['pass1'])
        pass_2 = escape(request.form['pass2'])

        
        if pass_1 != pass_2:
            return "Las contraseñas no coinciden"
        else:
            hash_clave = generate_password_hash(pass_1)
            try:
                with sqlite3.connect("DB_Clinica_RC.db") as con:
                    cur = con.cursor()

                    existe = cur.execute(
                        "SELECT Nombre_usuario FROM Pacientes WHERE Nombre_usuario=?", [user]).fetchone()

                    if existe!= None:
                        return "El Usuario ya existe, por favor intente de nuevo"
                    else:             
                        cur.execute("INSERT INTO Pacientes (Nombre,Apellido, Documento, Fecha_nac, Genero, Email, Residencia, Ciudad, Telefono, Nombre_usuario,Contraseña) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                           name, apell, docum, fecha_nac, gen, email, resid, ciudad, tel, user, hash_clave))
                        con.commit()
                        return "Guardado con exito"
                        #render_template('login.html')

            except Error:
                print(Error)
                return "Registro no completado"

    return render_template('register_paciente.html')


@app.route('/register_medico', methods=('GET', 'POST'))
def register_medico():
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
        espe = escape(request.form['espec'])
        pass_1 = escape(request.form['pass1'])
        pass_2 = escape(request.form['pass2'])

        
        if pass_1 != pass_2:
            return "Las contraseñas no coinciden"
        else:
            hash_clave = generate_password_hash(pass_1)
            try:
                with sqlite3.connect("DB_Clinica_RC.db") as con:
                    cur = con.cursor()

                    existe = cur.execute(
                        "SELECT Nombre_usuario FROM Medicos WHERE Nombre_usuario=?", [user]).fetchone()

                    if existe!= None:
                        return "El Usuario ya existe, por favor intente de nuevo"
                    else:             
                        cur.execute("INSERT INTO Medicos (Nombre,Apellido, Documento, Fecha_nac, Genero, Email, Residencia, Ciudad, Telefono, Especialidad, Nombre_usuario,Contraseña) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                           name, apell, docum, fecha_nac, gen, email, resid, ciudad, tel, espe, user, hash_clave))
                        con.commit()
                        return "Guardado con exito"
                        #return render_template('login.html')

            except Error:
                print(Error)
                #flash("Registro no completado")
                return "Registro no completado"

    return render_template('register_medico.html')



@app.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")

@app.route('/register_tipo_user')
def reg_user():
    return render_template("register_tipo_user.html")


@app.route('/login_correcto', methods=['GET'])
def login_correcto():
    if 'user' in session:
        try:
            with sqlite3.connect("DB_Clinica_RC.db") as con:

                con.row_factory = sqlite3.Row
                cur = con.cursor()
                query = cur.execute("SELECT Nombre, Email, Genero FROM Pacientes WHERE Nombre_usuario=?", [
                                    session['user']]).fetchone()

                if query is None:
                    return("El usuario no existe")

        except Error:
            print(Error)

        return render_template('login_correcto.html', name=query[0], email=query[1], gen=query[2])
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