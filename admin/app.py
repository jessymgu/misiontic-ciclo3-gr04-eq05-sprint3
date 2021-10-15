import os
from types import MethodDescriptorType
from flask import Flask, render_template, flash, url_for, request, redirect
import yagmail as yagmail
import utils
from forms import FormInicio

app = Flask(__name__) # __name__ busca archivos estáticos
app.secret_key = os.urandom(24)

url_for.__init__
@app.route('/')
def index():
    return render_template('index_temporal.html')

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
        flash(f"Inicio de sesión solicitada por el usuario {form.usuario.data}")
        return redirect(url_for("login_init"))
    return render_template("login.html", form=form)

@app.route("/login_correcto")
def login_init():
    return render_template("login_correcto.html")


@app.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            password = request.form['password']
            email = request.form['correo']
            error = None

            if not utils.isUsernameValid(nombre):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
                return render_template('register.html')

            if not utils.isUsernameValid(apellidos):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
                return render_template('register.html')

            if not utils.isPasswordValid(password):
                error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
                flash(error)
                return render_template('register.html')

            if not utils.isEmailValid(email):
                error = 'Correo invalido'
                flash(error)
                return render_template('register.html')
                
            #modificar la siguiente linea con tu informacion personal
            yag = yagmail.SMTP('pruebamintic2022', 'Jmd12345678') 
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bienvenido, usa este link para activar tu cuenta ')
            flash('Revisa tu correo para activar tu cuenta')
            return render_template('login.html')
        
        #print("Llego al final")
        return render_template('register.html')
    except:
        return render_template('register.html')
# Fin Rutas - AndrésCC 


if __name__ == '__main__': #activar modo debug
    app.run(debug=True)