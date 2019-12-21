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
    imagesurl=db.Column(db.String(200))
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
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False) 
    compositeur=db.Column(db.Boolean, default=False) 
    avatar=db.Column(db.String(128), nullable=False, default='default.png')
    articles = db.relationship('Article', backref='user_article', lazy='dynamic')
    partitions = db.relationship('Partition', backref='user_partition', lazy='dynamic')
    downloads= db.relationship('Download', backref='user_download', lazy='dynamic')
    

    def __repr__(self):
        return ' {} '.format(self.nom)

class Partition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_parti= db.Column(db.String(128))
    pdf_url = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    statut=db.Column(db.Boolean, default=False) 
    downloads = db.relationship('Download', backref='download_partition', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.titre_parti)

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nbr_download= db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    partition_id = db.Column(db.Integer, db.ForeignKey('partition.id'), nullable=False)
    statut=db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return ' {} '.format(self.titre_parti)


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False)  
    partitions = db.relationship('Partition', backref='type_partition', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

