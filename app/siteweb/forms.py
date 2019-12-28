from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Album, Partition, User, Types 

def rech_album():
    return Album.query.filter_by(statut=True).all()

def rech_part():
    return Partition.query.filter_by(statut=True).all()

def rech_user():
    return User.query.filter_by(statut=True, compositeur=True).all()

def rech_type():
    return Types.query.filter_by(statut=True).all()

class AlbumForm(FlaskForm):
    cate_pub= QuerySelectField(query_factory=rech_album, get_label='nom', allow_blank=False)
    submit = SubmitField('Chercher')

class PartForm(FlaskForm):
    partition= QuerySelectField(query_factory=rech_part, get_label='titre_parti', allow_blank=True, default='Tous')
    user_comp= QuerySelectField(query_factory=rech_user, get_label='prenom', allow_blank=True, default='Tous')
    types_part= QuerySelectField(query_factory=rech_type, get_label='nom', allow_blank=True, default='Tous')
    submit = SubmitField('Chercher')
   