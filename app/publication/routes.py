from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article 
from app.publication.forms import AjoutPForm, EditPForm
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify, Slugify, UniqueSlugify
from sqlalchemy.sql import func
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from . import publication

""" Ajout d'une publication sur la plate forme """

@publication.route('/ajouter_publication', methods=['GET', 'POST'])
@login_required
def ajouterpub():
   title='Publication'
   #Formulaire
   form=AjoutPForm()

   if form.validate_on_submit():
      #Titre de slug
      titre_slugify = Slugify(to_lower=True) #Slug
      titre=titre_slugify(form.titre.data)
      #gestion des documents transmis
      if form.document_pu.data:
         file_to_upload=form.document_pu.data
         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         save_publication=Article(titre=form.titre.data.capitalize(), slug=titre, resume=form.resume.data, document_pu=pdf_download, categorie_id=form.cate_pub.data.id, user_id=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la publication avec succès",'succes')
         return redirect(url_for('publication.lipub'))
      save_publication=Article(titre=form.titre.data.capitalize(), slug=titre, resume=form.resume.data, 
                              categorie_id=form.cate_pub.data.id, user_article=current_user)
      db.session.add(save_publication)
      db.session.commit()
      flash("Ajout de la publication avec succès",'succes')
      return redirect(url_for('publication.lipub'))
      
   return render_template('publication/ajpub.html', form=form, title=title)

""" énumeration des publication  """

@publication.route('/lis_pub', methods=['GET', 'POST'])
@login_required
def lipub():   
   #Titre
   title='Publication'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   pub_page=Article.query.order_by(Article.id.asc()).paginate(page=page, per_page=50)
    
   return render_template('publication/views.html', title=title, liste=pub_page)

""" Activation du statut de la publication """

@publication.route('/statut_pub/<int:pub_id>', methods=['GET', 'POST'])
@login_required
def statutpub(pub_id):
   #Titre
   title='Publication'

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification de la publication
   pub_statu=Article.query.filter_by(id=pub_id).first()

   if pub_statu is None:
      return redirect(url_for('publication.lipub'))

   if pub_statu.statut == True:
      pub_statu.statut=False
      db.session.commit()
      flash("La publication est désactivée sur la plateforme",'success')
      return redirect(url_for('publication.lipub'))
   else:
      pub_statu.statut=True
      db.session.commit()
      flash("La publication est activée sur la plateforme",'success')
      return redirect(url_for('publication.lipub'))
   
   return render_template('user/views.html',title=title)


""" Modification de la publication  """

@publication.route('/edit_<int:pub_id>', methods=['GET', 'POST'])
@login_required
def editpub(pub_id):
   form=EditPForm()
   #Titre
   title='Publication'
   #Requête de vérification des articles
   pub_class=Article.query.filter_by(id=pub_id).first()
   if pub_class is None:
      return redirect(url_for('publication.lipub'))
   if form.validate_on_submit(): 
      #Titre de slug
      titre_slugify = Slugify(to_lower=True) #Slug
      titre=titre_slugify(form.ed_titre.data)
      #gestion des documents transmis
      if form.ed_document_pu.data:
         file_to_upload=form.ed_document_pu.data
         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         pub_class.document_pdf=pdf_download
         pub_class.titre=form.ed_titre.data.capitalize()
         pub_class.slug=titre
         pub_class.resume=form.ed_resume.data
         pub_class.categorie_id=form.ed_cate_pub.data.id
         db.session.commit()
         flash("Modification réussie",'success')
         return redirect(url_for('publication.lipub'))
      #Modification des données
      pub_class.titre=form.ed_titre.data.capitalize()
      pub_class.slug=titre
      pub_class.resume=form.ed_resume.data
      pub_class.categorie_id=form.ed_cate_pub.data.id
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('publication.lipub'))
      
   if request.method=='GET':
      form.ed_titre.data=pub_class.titre
      form.ed_resume.data=pub_class.resume
      form.ed_cate_pub.data=pub_class.categorie_article.nom
   return render_template('publication/editpub.html', form=form, title=title)

