from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Statpage 
from app.statpage.forms import AjoutPForm, EditPForm
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify, Slugify, UniqueSlugify
from sqlalchemy.sql import func
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from . import statpage

""" Ajout d'une publication sur la plate forme """

@statpage.route('/ajouter_statpage', methods=['GET', 'POST'])
@login_required
def ajouterstatpage():
   title='Page statique'

   #Autorisation administrateur
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Formulaire
   form=AjoutPForm()

   if form.validate_on_submit():
      titre=form.titre.data.capitalize()
      enre=Statpage(titre=titre, contenu=form.contenu.data, user_pages=current_user)
      db.session.add(enre)
      db.session.commit()
      flash("Vous avez ajouté {}".format(titre),'success')
      return redirect(url_for('statpage.lipage'))

   return render_template('statpage/ajpage.html', form=form, title=title)

""" énumeration des pages  """

@statpage.route('/listepage', methods=['GET', 'POST'])
@login_required
def lipage():   
   #Titre
   title='Les pages'
   #Autorisation administrateur
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Requet des pagination et des listage des pages
   pages=Statpage.query.all()
   
   return render_template('statpage/views.html', title=title, liste=pages)

""" Modification de la page  """

@statpage.route('/edit_<int:pag_id>', methods=['GET', 'POST'])
@login_required
def editpage(pag_id):
   form=EditPForm()
   #Titre
   title='Modification'

    #Autorisation administrateur
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification des pages
   pub_class=Statpage.query.filter_by(id=pag_id).first()
   if pub_class is None:
      return redirect(url_for('publication.lipub'))

   if form.validate_on_submit(): 
      if form.ed_titre.data == pub_class.titre:
         pub_class.contenu=form.ed_contenu.data
         db.session.commit()
         flash("La modification avec succès",'success')
         return redirect(url_for('statpage.lipage'))
      else:
         pub_class.titre=form.ed_titre.data.capitalize()
         pub_class.contenu=form.ed_contenu.data
         db.session.commit()
         flash("La modification avec succès",'success')
         return redirect(url_for('statpage.lipage'))

   if request.method=='GET':
      form.ed_titre.data=pub_class.titre
      form.ed_contenu.data=pub_class.contenu
      
   return render_template('statpage/editpage.html', form=form, title=title)

