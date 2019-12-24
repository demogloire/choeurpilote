from flask import render_template, flash, url_for, redirect, request, session, send_file
from .. import db, bcrypt
from ..models import User, Partition
from app.partition.forms import AjoutPartForm, EdiPartForm
from flask_login import login_user, current_user, logout_user, login_required
from slugify import slugify, Slugify, UniqueSlugify
from sqlalchemy.sql import func
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from . import partition

""" Ajout d'une publication sur la plate forme """

@partition.route('/ajouter_partition', methods=['GET', 'POST'])
@login_required
def ajouterpart():
   title='Partition de la messe | CPPCU'
   #Formulaire
   form=AjoutPartForm()

   if form.validate_on_submit():
      #Les variables vide
      pdf_download=None
      #gestion des documents transmis
      if form.document_pu.data:
         file_to_upload=form.document_pu.data
         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         save_publication=Partition(titre_parti=form.titre.data,type_id=form.type_part.data.id,pdf_url=pdf_download,user_partition=current_user)
         db.session.add(save_publication)
         db.session.commit()
         flash("Ajout de la partition avec succès",'success')
         return redirect(url_for('partition.lipuart'))
      else:
         flash("Attention",'danger')
         
   return render_template('partition/ajpub.html', form=form, title=title)

""" énumeration des partitions """

@partition.route('/lis_part', methods=['GET', 'POST'])
@login_required
def lipuart():   
   #Titre
   title='Partition de la messe | CPPCU'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   pub_page=Partition.query.order_by(Partition.id.asc()).paginate(page=page, per_page=50)
    
   return render_template('partition/views.html', title=title, liste=pub_page)


@partition.route('/lis_part/<int:part_id>', methods=['GET', 'POST'])
@login_required
def telechargement(part_id):   
   #Titre
   title='Partition de la messe | Choeur Pilote'
   #Requête de vérification de la partition
   part_li=Partition.query.filter_by(id=part_id).first()
   #Partition
   if part_li is None:
      return redirect(url_for('partition.lipuart'))
   return redirect(part_li.pdf_url)

""" Statut de la partition """

@partition.route('/statut_part/<int:part_id>', methods=['GET', 'POST'])
@login_required
def statutpart(part_id):
   #Titre
   title='Partition de la messe | CPPCU'
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Requête de vérification de la partition
   pub_statu=Partition.query.filter_by(id=part_id).first()

   if pub_statu is None:
      return redirect(url_for('partition.lipuart'))

   if pub_statu.statut == True:
      pub_statu.statut=False
      db.session.commit()
      flash("La partition est désactivée sur la plateforme",'success')
      return redirect(url_for('partition.lipuart'))
   else:
      pub_statu.statut=True
      db.session.commit()
      flash("La partition est activée sur la plateforme",'success')
      return redirect(url_for('partition.lipuart'))
   
   return render_template('user/views.html',title=title)



""" Statut de la partition """

@partition.route('/edit_<int:part_id>', methods=['GET', 'POST'])
@login_required
def editpart(part_id):

   title='Partition de la messe | CPPCU' 
   #Partition
   part_class=Partition.query.filter_by(id=part_id).first()
   #Si la partition ne pas trouver
   if part_class is None:
      return redirect(url_for('partition.lipuart'))
   #Si tu ne pas proprietaire
   if part_class.user_id != current_user.id:
      return redirect(url_for('partition.lipuart'))
         
   #Formulaire 
   form=EdiPartForm()
   if form.validate_on_submit():
          #Les variables vide
      pdf_download=None
      #gestion des documents transmis
      if form.document_pu.data:
         file_to_upload=form.document_pu.data
         if file_to_upload:
            try:
               upload_result = upload(file_to_upload)
            except:
               flash("Erreur de connexion",'danger')

         pdf_download=upload_result['url'] # Mise en route du fichier pdf
         part_class.pdf_url=pdf_download
         part_class.titre_parti=form.titre.data
         part_class.type_id=form.type_part.data.id
         part_class.statut=False
         db.session.commit()
         flash("Modification avec succès",'success')
         return redirect(url_for('partition.lipuart'))

      else:
         part_class.titre_parti=form.titre.data
         part_class.type_id=form.type_part.data.id
         part_class.statut=False
         db.session.commit()
         flash("Modification avec succès",'success')
         return redirect(url_for('partition.lipuart'))
  
   if request.method=='GET':
          
      form.titre.data=part_class.titre_parti
      form.type_part.data=part_class.type_partition.nom
      
   return render_template('partition/editpub.html', form=form, title=title)

