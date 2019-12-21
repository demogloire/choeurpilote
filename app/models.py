from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False)  
    articles = db.relationship('Article', backref='categorie_article', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    resume = db.Column(db.Text)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slug=db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False) 
    document_pdf=db.Column(db.String(200))
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    def __repr__(self):
        return ' {} '.format(self.titre)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    role = db.Column(db.String(128))
    domaine = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False) 
    organisation = db.Column(db.String(60))
    avatar=db.Column(db.String(128), nullable=False, default='default.png')
    articles = db.relationship('Article', backref='user_article', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.nom)

class Wificode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_username = db.Column(db.String(128))
    code_password = db.Column(db.String(128))
    code_validation=db.Column(db.String(1))
    debut_validation= db.Column(db.String(128))
    fin_validation = db.Column(db.String(128))
    adresse_mac = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return ' {} '.format(self.code_username)

