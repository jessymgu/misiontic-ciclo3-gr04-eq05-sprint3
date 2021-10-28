from types import MethodDescriptorType
from flask import Flask, render_template, url_for,request, session
from markupsafe import escape
import os
import sqlite3
from sqlite3 import Error
from flask.helpers import flash
app = Flask(__name__) # __name__ busca archivos estáticos

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

# ----------------------------------------------------------------paciente citas--------------------------------#
@app.route('/citas-paciente', methods=["GET"])
def citaspaciente():
    try:
        with sqlite3.connect('citasmedico.db') as con:
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
             with sqlite3.connect('citasmedico.db') as con:
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
        with sqlite3.connect('citasmedico.db') as con:
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


# -------------------------------------------------perfiles de usuario---------------------------------------------#
    # !Luego, el administrador, si así lo decide, usando el método POST, envía información a la BD. Puesto que el superadministrador puede crear una nueva cita, editar, o eliminar su información. Para ello, envía la información desde el navegador hasta el servidor (crear, editar o eliminar)
@app.route('/medico-perfil', methods=["GET", "POST"])
def medico_perfil():
    return render_template('perfil_medico.html')

@app.route('/paciente-perfil', methods=["GET", "POST"])
def paciente_perfil():
    return render_template('perfil_paciente.html')



if __name__ == '__main__': #activar modo debug
    app.run(debug=True)