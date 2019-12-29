from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article 
from app.publication.forms import AjoutPForm, EditPForm, AjoutPIForm, AjoutPPForm
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
      #Les variables vide
      pdf_download=None
      img_download=None

      #gestion des documents transmis
      if form.document_pu.data and form.document_img.data:
         file_to_upload=form.document_pu.data
         img_file_to_upload=form.document_img.data

         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         if img_file_to_upload:
            try:
               img_upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         img_download=img_upload_result['url'] # Mise en route du fichier pdf

         save_publication=Article(titre=form.titre.data.capitalize(), imagesurl=img_download, slug=titre, resume=form.resume.data, document_pdf=pdf_download, categorie_id=form.cate_pub.data.id, user_article=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la publication avec succès",'success')
         return redirect(url_for('publication.lipub'))

      elif form.document_pu.data:
         file_to_upload=form.document_pu.data
         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         
         save_publication=Article(titre=form.titre.data.capitalize(), slug=titre, resume=form.resume.data, document_pdf=pdf_download, categorie_id=form.cate_pub.data.id, user_article=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la publication avec succès",'success')
         return redirect(url_for('publication.lipub'))

      elif form.document_img.data:
         img_file_to_upload=form.document_img.data

         if img_file_to_upload:
            try:
               img_upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         img_download=img_upload_result['url'] # Mise en route du fichier pdf

         save_publication=Article(titre=form.titre.data.capitalize(), imagesurl=img_download, slug=titre, resume=form.resume.data, categorie_id=form.cate_pub.data.id, user_article=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la publication avec succès",'success')
         return redirect(url_for('publication.lipub'))
      else:
         save_publication=Article(titre=form.titre.data.capitalize(), slug=titre, resume=form.resume.data, 
                              categorie_id=form.cate_pub.data.id, user_article=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la publication avec succès",'success')
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
   #Les variables
   img_upload_result=None
   upload_result=None

   if pub_class is None:
      return redirect(url_for('publication.lipub'))
   if form.validate_on_submit(): 
      #Titre de slug
      titre_slugify = Slugify(to_lower=True) #Slug
      titre=titre_slugify(form.ed_titre.data)
      #gestion des documents transmis
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



@publication.route('/image_mod_img/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def modpubimg(cate_id):
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title="Image publication | Choeur Pilote"
   #formulaire
   form=AjoutPIForm()

   upload_result=None

   pub_class=Article.query.filter_by(id=cate_id).first_or_404()
   #De nom de l'album
   nom_album=pub_class.titre
   #Le nom du type encours de modification
   if pub_class is None:
      return redirect(url_for('publication.lipub'))

   if form.validate_on_submit():
      if form.file.data:
         img_file_to_upload=form.file.data

         if img_file_to_upload:
            try:
               upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
               return redirect(url_for('publication.modpubimg', cate_id=cate_id))
         img_download=upload_result['url'] # Mise en route du fichier jpg
         #Enregistrement des informations dans la base des données
         pub_class.imagesurl=img_download   
         db.session.commit()
         flash("Mise à jour avec succès", "success")
         return redirect(url_for('publication.lipub')) 
         

   return render_template('publication/ulpload_img.html',nom_album=nom_album,  title=title, form=form)

   
@publication.route('/image_mod_pdf/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def modpubpdf(cate_id):
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title="PDF de la publication | Choeur Pilote"
   #formulaire
   form=AjoutPPForm()

   upload_result=None

   pub_class=Article.query.filter_by(id=cate_id).first_or_404()
   #De nom de l'album
   nom_album=pub_class.titre
   #Le nom du type encours de modification
   if pub_class is None:
      return redirect(url_for('publication.lipub'))

   if form.validate_on_submit():
      if form.file.data:
         img_file_to_upload=form.file.data

         if img_file_to_upload:
            try:
               upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
               return redirect(url_for('publication.modpubimg', cate_id=cate_id))
         img_download=upload_result['url'] # Mise en route du fichier jpg
         #Enregistrement des informations dans la base des données
         pub_class.document_pdf=img_download   
         db.session.commit()
         flash("Mise à jour avec succès", "success")
         return redirect(url_for('publication.lipub')) 
         

   return render_template('publication/ulpload_pdf.html',nom_album=nom_album,  title=title, form=form)

   
