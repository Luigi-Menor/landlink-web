from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo electrónico es requerido'),
        Email(message='Ingrese un correo electrónico válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida')
    ])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión') 