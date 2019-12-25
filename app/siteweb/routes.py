from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article, Categorie, Statpage 
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

@siteweb.route('/quisommes-nous.html', methods=['GET', 'POST'])
def quisommes():
   title='Qui sommes-nous?'
   #Page
   page='Qui sommes-nous?'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Apropos
   apropos='apropos'
   
   return render_template('siteweb/apropos/quisommes.html', apropos=apropos, title=title, rec=qui_id)


@siteweb.route('/historique.html', methods=['GET', 'POST'])
def historique():
   #Page
   page='Historique'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Titre de la page
   title=qui_id.titre
   #Apropos
   apropos='apropos'

   return render_template('siteweb/apropos/historique.html', apropos=apropos, title=title, rec=qui_id)

@siteweb.route('/prospectif.html', methods=['GET', 'POST'])
def prospectif():
   #Page
   page='Prospectif'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Titre de la page
   title=qui_id.titre
   #Apropos
   apropos='apropos'

   return render_template('siteweb/apropos/prospectif.html', apropos=apropos, title=title, rec=qui_id)

@siteweb.route('/comiteduchoeur.html', methods=['GET', 'POST'])
def comite():
   #Titre de la page
   title='Le comité du choeur'
   rec=None
   #Apropos
   apropos='apropos'

   return render_template('siteweb/apropos/comite.html', rec=rec, apropos=apropos, title=title)


@siteweb.route('/agenda.html', methods=['GET', 'POST'])
def agenda():
   #Page
   page='Agenda'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Titre de la page
   title=qui_id.titre
   #Apropos
   apropos='apropos'

   return render_template('siteweb/otherpage/agenda.html', apropos=apropos, title=title, rec=qui_id)
