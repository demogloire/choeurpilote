from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Categorie

def rech_type():
    return Types.query.all()

class AjoutCatForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    submit = SubmitField('Categorie')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_nom(self, nom):
        type= Categorie.query.filter_by(nom=nom.data).first()
        if type:
            raise ValidationError("Cette catégorie existe déjà")

class EditCatForm(FlaskForm):
    ed_nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_submit = SubmitField('Classification')


class AjoutPhoForm(FlaskForm):
    file = FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
    submit = SubmitField('Publier')

class AjoutEdPForm(FlaskForm):
    file = FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
    submit = SubmitField('Publier')