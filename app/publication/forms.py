from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Categorie

def rech_cat():
    return Categorie.query.filter_by(statut=True)

class AjoutPForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    resume= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    document_pu = FileField('Document', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    document_img = FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
    cate_pub= QuerySelectField(query_factory=rech_cat, get_label='nom', allow_blank=False)
    submit = SubmitField('Publier')

class EditPForm(FlaskForm):
    ed_titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    ed_resume= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    ed_document_pu = FileField('Document', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    ed_document_img = FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
    ed_cate_pub= QuerySelectField(query_factory=rech_cat, get_label='nom', allow_blank=False)
    submit = SubmitField('Publier')
