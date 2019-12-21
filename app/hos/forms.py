from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User


class LoginHostForm(FlaskForm):
    code_username= StringField('Email', validators=[DataRequired('Votre code')])
    code_password= PasswordField('Mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe')])
    submit = SubmitField('Créer compte')
