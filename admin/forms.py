from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired,Length

class FormInicio(FlaskForm):
    usuario =StringField('Usuario o email', validators=[DataRequired(message="completar campo"), Length(max=10)])
    contrasena =PasswordField('Contraseña', validators=[DataRequired(message="completar campo")])
    recordar =BooleanField('Recordar inicio de sesión')
    enviar =SubmitField('Enviar')