from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article 
#from app.user.forms import AjouteruserForm, PassuserForm, EditeruserForm
from flask_login import login_user, current_user, logout_user, login_required
from . import main

@main.route('/administration', methods=['GET', 'POST'])
@login_required
def dashboard():
   title='Dashboard'
   nombre_user=User.query.filter_by(role='Webmaster').all()
   nombre_arti=Article.query.all()
   #Tableau de comptage
   clients=[]
   article=[]
   #Nombre de client
   for client in nombre_user:
      i=client.id
      clients.insert(0,i)
   nbr_client=len(clients)
   #Nombre des articles
   for articles in nombre_arti:
      i=articles.id
      article.insert(0,i)
   nbr_article=len(article)

   return render_template('main/main.html',  title=title, user_client=nbr_client, user_article=nbr_article)

@main.route('/configuration', methods=['GET', 'POST'])
@login_required
def config():
   title='Dashboard'
   return render_template('main/conf.html',  title=title)

@main.route('/conf_produit', methods=['GET', 'POST'])
@login_required
def configpro():
   title='Dashboard | Kivu Exchange'
   return render_template('main/confpro.html',  title=title)