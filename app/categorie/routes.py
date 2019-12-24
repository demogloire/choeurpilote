from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Categorie
from app.categorie.forms import AjoutCatForm, EditCatForm
from flask_login import login_user, current_user, logout_user, login_required
from . import categorie



''' Ajoute une categorisation '''

@categorie.route('/ajou_categorie', methods=['GET', 'POST'])
@login_required
def ajoutcate():

   #autorisation par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Titre 
   title='Catégorie publication | Choeur Pilote'
   #formulaire
   form=AjoutCatForm()

   if form.validate_on_submit():
      nom_cat=form.nom.data.capitalize()
      categorie_enre=Categorie(nom=nom_cat)
      db.session.add(categorie_enre)
      db.session.commit()
      flash("Ajout avec succès une nouvelle categorisation",'success')
      return redirect(url_for('categorie.litcate')) 

   return render_template('categorie/ajouter.html',  title=title, form=form)


""" Liste des categories"""
@categorie.route('/lis_categorie', methods=['GET', 'POST'])
@login_required
def litcate():
   #autorisation par administrateur
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Titre
   title='Catégorie publication | Choeur Pilote'
   #Requête d'affichage de la categorisation
   listes=Categorie.query.order_by(Categorie.id.desc())
   return render_template('categorie/views.html',title=title, liste=listes)



""" Modifier catégorisation """

@categorie.route('/statut_cate/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def statutcat(cat_id):
   #Titre
   title='Catégorie publication | Choeur Pilote'
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification de la categorie
   cat_statu=Categorie.query.filter_by(id=cat_id).first()

   if cat_statu is None:
      return redirect(url_for('categorie.litcate'))

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      flash("La catégorie est désactivée sur la plateforme",'success')
      return redirect(url_for('categorie.litcate'))
   else:
      cat_statu.statut=True
      db.session.commit()
      flash("La catégorie est activée sur la plateforme",'success')
      return redirect(url_for('categorie.litcate'))
   
   return render_template('user/views.html',title=title)


""" Modification de la catégorie  """

@categorie.route('/edit_<int:cate_id>_cate', methods=['GET', 'POST'])
@login_required
def editcate(cate_id):
       
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))       
   
   form=EditCatForm()
   #Titre
   title='Catégorie publication | Choeur Pilote'
   #Requête de vérification du type
   cate_class=Categorie.query.filter_by(id=cate_id).first()
   #Le nom du type encours de modification
   cate_nom=cate_class.nom

   if cate_class is None:
      return redirect(url_for('categorie.litcate'))
   
   if form.validate_on_submit(): 
      cate_class.nom=form.ed_nom.data.capitalize()
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('categorie.litcate'))
      
   if request.method=='GET':
      form.ed_nom.data=cate_class.nom
      
   return render_template('categorie/editcat.html', form=form, title=title, cate_nom=cate_nom)

