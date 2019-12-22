from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Types

def rech_typ():
    return Types.query.filter_by(statut=True)

class AjoutPartForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    document_pu = FileField('Document', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    type_part= QuerySelectField(query_factory=rech_typ, get_label='nom', allow_blank=False)
    submit = SubmitField('Partition')

class EdiPartForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=4, max=200, message="Veuillez respecté les caractères")])
    document_pu = FileField('Document', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    type_part= QuerySelectField(query_factory=rech_typ, get_label='nom', allow_blank=False)
    submit = SubmitField('Partition')
