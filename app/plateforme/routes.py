from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article
from app.fonction.fonction import login_session, getcookie
from flask_login import login_user, current_user, logout_user, login_required
from . import plateforme





@plateforme.route('/', methods=['GET', 'POST'])
def index():
   
 
   title='Bienvenue'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   pub_page=Article.query.filter_by(statut=True).order_by(Article.id.asc())
   recent_pub=Article.query.filter_by(statut=True).order_by(Article.id.desc()).limit(3)

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
   
   return render_template('plateforme/index.html',  title=title, liste=pub_page, rec=recent_pub, art_nbr=nbr_article, clie_nbr=nbr_client)

""" liste de publication """

@plateforme.route('/valve', methods=['GET', 'POST'])
def valve():
   


   title='Valve'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   pub_page=Article.query.filter_by(statut=True).order_by(Article.id.desc()).paginate(page=page, per_page=50)
   recent_pub=Article.query.filter_by(statut=True).order_by(Article.id.asc()).limit(3)
   
   return render_template('plateforme/valve.html',  title=title, liste=pub_page, rec=recent_pub)


""" Une publication sur la plateforme """

@plateforme.route('/publication/<string:id_slug>', methods=['GET', 'POST'])
def pub(id_slug):
       
   title='Publication'
   #Liste des articles publiés
   post_rec=Article.query.filter_by(slug=id_slug).first()
   if post_rec is None:
      return redirect(url_for('plateforme.index'))
   
   recent_pub=Article.query.filter_by(statut=True).order_by(Article.id.asc()).limit(3)

   return render_template('plateforme/post.html',  title=title, post=post_rec, rec=recent_pub)
