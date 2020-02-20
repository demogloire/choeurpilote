from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article, Partition, Media 
#from app.user.forms import AjouteruserForm, PassuserForm, EditeruserForm
from flask_login import login_user, current_user, logout_user, login_required
from . import main

@main.route('/administration', methods=['GET', 'POST'])
@login_required
def dashboard():
   title='Dashboard'

   nombre_arti=Article.query.all()
   nmbr_album=Media.query.all()
   nmbr_partition=Partition.query.all()
   #Tableau de comptage
   article=[]
   album=[]
   partition=[]
   partitions=[]
   #Les variables des controles
   nbr_article=0
   nbr_album=0
   nbr_part=0
   sommes_telecharger_part=0
   #Nombre des articles
   for articles in nombre_arti:
      i=articles.id
      article.insert(0,i)
   nbr_article=len(article)
   #Nombre des albums
   for album_com in nmbr_album:
      i=album_com.id
      album.insert(0,i)
   nbr_album=len(album)
   #Nombre des partitions
   for partition_pu in nmbr_partition:
      i=partition_pu.id
      partition.insert(0,i)
   nbr_part=len(partition)
   #Nombre des partitions téléchargées
   for partition_t in nmbr_partition:
      i=partition_t.nbr_download
      partitions.insert(0,i)
   sommes_telecharger_part=sum(partitions)
   #Les artciles non actifs
   nombre_article_pu=Article.query.filter_by(statut=False)
   controle_actif="Vide"
   if nombre_article_pu is not None:
      controle_actif="Novide"

  
      

   return render_template('main/main.html', nombre_article_pu=nombre_article_pu, controle_actif=controle_actif, title=title, nbr_article=nbr_article, nbr_album=nbr_album, nbr_part=nbr_part, sommes_telecharger_part=sommes_telecharger_part)

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