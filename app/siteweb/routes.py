from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article, Categorie 
#from app.user.forms import AjouteruserForm, PassuserForm, EditeruserForm
from flask_login import login_user, current_user, logout_user, login_required
from . import siteweb

@siteweb.route('', methods=['GET', 'POST'])
def index():
   title='Bienvenue'

   
   #Triage selon les articles
   cat_id=Categorie.query.filter_by(nom='Article').first()
   recent_pub=Article.query.filter_by(statut=True, categorie_id=cat_id.id).order_by(Article.id.desc()).limit(3)
   #Triage selon les communiquées
   comm_id=Categorie.query.filter_by(nom='Communiqué').first()
   recent_communiqu=Article.query.filter_by(statut=True, categorie_id=comm_id.id).all()
     
   return render_template('siteweb/index.html',  title=title, rec=recent_pub, recm=recent_communiqu)
