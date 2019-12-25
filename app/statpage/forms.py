from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Statpage

def rech_cat():
    return Categorie.query.filter_by(statut=True)

class AjoutPForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    contenu= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    submit = SubmitField('Page')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_titre(self, titre):
        titre= Statpage.query.filter_by(titre=titre.data).first()
        if titre:
            raise ValidationError("Cette page existe déjà")

class EditPForm(FlaskForm):
    ed_titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    ed_contenu= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    submit = SubmitField('Page')
    

    