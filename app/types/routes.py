from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Types
from app.types.forms import AjoutTypeForm, EditTypeForm
from flask_login import login_user, current_user, logout_user, login_required
from . import types



''' Ajoute une categorisation '''

@types.route('/ajou_types', methods=['GET', 'POST'])
@login_required
def ajouttype():

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Titre 
   title='Partie de la messe | CPPCU'
   #formulaire
   form=AjoutTypeForm()

   if form.validate_on_submit():
      nom_type=form.nom.data.capitalize()
      type_enre=Types(nom=nom_type)
      db.session.add(type_enre)
      db.session.commit()
      flash("Ajout de partie de la messe avec succès",'success')
      return redirect(url_for('types.littype'))

   return render_template('types/ajouter.html',  title=title, form=form)


""" Liste des categories"""
@types.route('/lis_types', methods=['GET', 'POST'])
@login_required
def littype():
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Titre
   title='Partie de la messe | CPPCU'
   #Requête d'affichage de la categorisation
   listes=Types.query.order_by(Types.id.desc())
   return render_template('types/views.html',title=title, liste=listes)



""" Modifier catégorisation """

@types.route('/statut_type/<int:type_id>', methods=['GET', 'POST'])
@login_required
def statuttype(type_id):
   #Titre
   title='Partie de la messe| CPPCU'

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification de la categorie
   cat_statu=Types.query.filter_by(id=type_id).first()

   if cat_statu is None:
      return redirect(url_for('types.littype'))

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      flash("La partie de la messe est desactivée",'success')
      return redirect(url_for('types.littype'))
   else:
      cat_statu.statut=True
      db.session.commit()
      flash("La partie de la messe est activée",'success')
      return redirect(url_for('types.littype'))
   
   return render_template('types/views.html',title=title)


""" Modification de la catégorie  """

@types.route('/edit_<int:type_id>_cate', methods=['GET', 'POST'])
@login_required
def editype(type_id):
       
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))       
   
   form=EditTypeForm()
   #Titre
   title='Partie de la messe| CPPCU'
   #Requête de vérification du type
   cate_class=Types.query.filter_by(id=type_id).first()
   #Le nom du type encours de modification
   cate_nom=cate_class.nom

   if cate_class is None:
      return redirect(url_for('types.littype'))
   
   if form.validate_on_submit(): 
      cate_class.nom=form.ed_nom.data.capitalize()
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('types.littype'))
      
   if request.method=='GET':
      form.ed_nom.data=cate_class.nom
      
   return render_template('types/editcat.html', form=form, title=title, cate_nom=cate_nom)

