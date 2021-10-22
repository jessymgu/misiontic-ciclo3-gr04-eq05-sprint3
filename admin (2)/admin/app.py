from types import MethodDescriptorType
from flask import Flask, render_template, url_for
app = Flask(__name__) # __name__ busca archivos estáticos

# @app.route("/")
@app.route('/superadmin')
@app.route("/superadmin-dashboard", methods=["GET"])
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

@app.route('/resultados_busqueda', methods=["GET"])
def resultados_busqueda():
    return render_template('resultado.html')

if __name__ == '__main__': #activar modo debug
    app.run(debug=True)