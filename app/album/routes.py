from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Categorie, Album, Media
from app.album.forms import AjoutCatForm, EditCatForm, AjoutPhoForm, AjoutEdPForm
from flask_login import login_user, current_user, logout_user, login_required
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from . import album

from app.album.utilities import upload_acif, upload_inactif



''' Ajoute d'un album '''

@album.route('/ajou_album', methods=['GET', 'POST'])
@login_required
@upload_inactif
def ajoutalbm():

   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title="Création d'album | Choeur Pilote"
   #formulaire
   form=AjoutCatForm()

   if form.validate_on_submit():
      nom_cat=form.nom.data.capitalize()
      album_enre=Album(nom=nom_cat)
      db.session.add(album_enre)
      db.session.commit()
      session['album'] = album_enre.id
      session['nom_album']=album_enre.nom
      return redirect(url_for('album.mediaalbm')) 
   return render_template('album/ajouter.html',  title=title, form=form)


@album.route('/media_ajout', methods=['GET', 'POST'])
@login_required
@upload_acif
def mediaalbm():
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title="Média | Choeur Pilote"
   #formulaire
   form=AjoutPhoForm()

   upload_result=None

   #Les information de l'album encours d'enregistrements
   if 'album' in session and 'nom_album' in session:
      id_album=session['album']
      nom_album=session['nom_album']

   if form.validate_on_submit():
      if form.file.data:
         img_file_to_upload=form.file.data

         if img_file_to_upload:
            try:
               upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
         img_download=upload_result['url'] # Mise en route du fichier jpg

         
         #Enregistrement des informations dans la base des données
         enre_media=Media(imagesurl=img_download, album_id=id_album)
         db.session.add(enre_media)
         db.session.commit()
         flash("Vous avez ajouté une image dans votre album", "success")
         return redirect(url_for('album.mediaalbm')) 
         

   return render_template('album/ulpload_img.html',nom_album=nom_album,  title=title, form=form)


""" Liste des albums"""
@album.route('/lisalbum', methods=['GET', 'POST'])
@login_required
def listalbum():
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))
   #Titre
   title='Liste des albums | Choeur Pilote'
   #Requête d'affichage de la categorisation
   listes=Album.query.order_by(Album.id.desc())
   return render_template('album/views.html',title=title, liste=listes)



"""Activation d'album """

@album.route('/statut_album/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def statutalb(cat_id):
   #Titre
   title="L'album | Choeur Pilote"
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification de l'album
   cat_statu=Album.query.filter_by(id=cat_id).first_or_404()

   if cat_statu is None:
      return redirect(url_for('album.listalbum')) 

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      flash("L'album est désactivé sur la plateforme",'success')
      return redirect(url_for('album.listalbum')) 
   else:
      cat_statu.statut=True
      db.session.commit()
      flash("L'album est activée sur la plateforme",'success')
      return redirect(url_for('album.listalbum'))
   
   return render_template('user/views.html',title=title)

@album.route('finupload', methods=['GET', 'POST'])
def terminerupload():
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   if 'album' in session:
      session.pop('album', None)
      return redirect(url_for('album.listalbum'))
   else:
      return redirect(url_for('album.listalbum'))
          
   return render_template('siteweb/otherpage/agenda.html', apropos=apropos, title=title, rec=qui_id)


# """ Modification de la catégorie  """

@album.route('/edit_<int:cate_id>_cate', methods=['GET', 'POST'])
@login_required
def editalbum(cate_id):
       
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))   
   
   form=EditCatForm()
   #Titre
   title="Modification de l'album | Choeur Pilote"
   #Requête de vérification de l'album
   cate_class=Album.query.filter_by(id=cate_id).first()
   #Le nom du type encours de modification
   cate_nom=cate_class.nom

   if cate_class is None:
      return redirect(url_for('album.listalbum'))
   
   
   if form.validate_on_submit(): 
      cate_class.nom=form.ed_nom.data.capitalize()
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('album.listalbum'))
      
   if request.method=='GET':
      form.ed_nom.data=cate_class.nom
      
   return render_template('album/edit.html', form=form, title=title, cate_nom=cate_nom)


@album.route('/media_ajout/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def mediaaled(cate_id):
   #autorisation par l'administrateur.
   if current_user.compositeur == True  and current_user.role=='Compositeur':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title="Média | Choeur Pilote"
   #formulaire
   form=AjoutEdPForm()

   upload_result=None

   cate_class=Album.query.filter_by(id=cate_id).first_or_404()
   #De nom de l'album
   nom_album=cate_class.nom
   #Le nom du type encours de modification
   if cate_class is None:
      return redirect(url_for('album.listalbum'))


   if form.validate_on_submit():
      if form.file.data:
         img_file_to_upload=form.file.data

         if img_file_to_upload:
            try:
               upload_result = upload(img_file_to_upload)
            except:
               flash("Erreur de connexion",'danger')
         img_download=upload_result['url'] # Mise en route du fichier jpg
         #Enregistrement des informations dans la base des données
         enre_media=Media(imagesurl=img_download, album_id=cate_id)
         db.session.add(enre_media)
         db.session.commit()
         flash("Vous avez ajouté une image dans votre album", "success")
         return redirect(url_for('album.mediaaled')) 
         

   return render_template('album/ulpload_imgc.html',nom_album=nom_album,  title=title, form=form)

   


