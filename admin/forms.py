from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired,Length

class FormInicio(FlaskForm):
    username =StringField('Usuario', validators=[DataRequired(message="Completar campo alias"), Length(max=9)])
    password =PasswordField('Contraseña', validators=[DataRequired(message="Completar campo contraseña")])
    recordar =BooleanField('Recordar inicio de sesión')
    enviar =SubmitField('Enviar')