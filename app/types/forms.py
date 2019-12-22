from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Types

def rech_type():
    return Types.query.all()

class AjoutTypeForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    submit = SubmitField('Type')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_nom(self, nom):
        type= Types.query.filter_by(nom=nom.data).first()
        if type:
            raise ValidationError("Cette partie existe déjà")

class EditTypeForm(FlaskForm):
    ed_nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_submit = SubmitField('Classification')

