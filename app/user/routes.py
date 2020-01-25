from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User 
from app.user.forms import AjouteruserForm, PassuserForm, EditeruserForm
from flask_login import login_user, current_user, logout_user, login_required
from . import user


""" Ajout d'un nouveau user """

@user.route('/ajouteruti', methods=['GET', 'POST'])
@login_required
def ajuser():
       

   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Formulaire de service
   
   form=AjouteruserForm()
   #ENregfistrement des operations
   if form.validate_on_submit():
      nom=form.nom.data.upper()
      prenom=form.prenom.data.capitalize()
      post_nom=form.post_nom.data.upper()
      password_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')   
      utilisateur=User(nom=nom, prenom=prenom,post_nom=post_nom, password=password_hash, username=form.username.data,role=form.role.data)
      db.session.add(utilisateur)
      db.session.commit()
      flash("Ajout d'un utilisateur avec succès",'success')
      return redirect(url_for('user.liuser')) 
   return render_template('user/ajuser.html', form=form)


""" Ajout Administrateur """

@user.route('/ajoutad', methods=['GET', 'POST'])
def ajouteruserad():
      
   form=AjouteruserForm()
   #ENregfistrement des operations
   if form.validate_on_submit():
      nom=form.nom.data.upper()
      prenom=form.prenom.data.capitalize()
      post_nom=form.post_nom.data.upper()
      password_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')   
      utilisateur=User(nom=nom, prenom=prenom,post_nom=post_nom, password=password_hash, username=form.username.data,role=form.role.data, statut=True, compositeur=True)
      db.session.add(utilisateur)
      db.session.commit()
      flash("Ajout de l'administrateur",'success')
      return redirect(url_for('auth.login')) 
   return render_template('user/ajuserad.html', form=form)


""" Liste utilisateur """

@user.route('/listeuti', methods=['GET', 'POST'])
#@login_required
def liuser():
   #Requête d'affichage des utlisateurs
   listes=User.query.order_by(User.id.desc())

   return render_template('user/views.html',liste=listes)


""" Modifier statut de l'Utilisateur """

@user.route('/statutut/<int:user_id>', methods=['GET', 'POST'])
#@login_required
def statutuser(user_id):
   #Titre
   title='Utilisateur | Choeur pilote'
   #Requête de vérification de l'utilisateur
   user_statu=User.query.filter_by(id=user_id).first()

   
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   
   if current_user.id== user_statu.id:
      return redirect(url_for('user.liuser'))
   
   if user_statu is None:
      return redirect(url_for('user.liuser'))

   if user_statu.statut == True:
      user_statu.statut=False
      db.session.commit()
      flash("l'utilisateur est désactivé sur la plateforme",'success')
      return redirect(url_for('user.liuser')) 
   else:
      user_statu.statut=True
      flash("l'utilisateur est activé sur la plateforme",'success')
      db.session.commit()
      return redirect(url_for('user.liuser')) 
   
   return render_template('user/views.html',title=title)

""" Compositeur """
@user.route('/compositeur/<int:user_id>', methods=['GET', 'POST'])
#@login_required
def compositeur(user_id):
   #Titre
   title='Activation'
   #Requête de vérification de l'utilisateur
   user_statu=User.query.filter_by(id=user_id).first()

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
      
   if user_statu is None:
      return redirect(url_for('user.liuser'))

   if user_statu.compositeur == True:
      user_statu.compositeur=False
      db.session.commit()
      flash("l'utilisateur ne plus compositeur",'success')
      return redirect(url_for('user.liuser')) 
   else:
      user_statu.compositeur=True
      flash("l'utilisateur est compositeur menant",'success')
      db.session.commit()
      return redirect(url_for('user.liuser')) 
   
   return render_template('user/views.html',title=title)


""" Modifier le mot de passé de l'utilisateur """

@user.route('/motdepass/<int:user_id>', methods=['GET', 'POST'])
#@login_required
def passuser(user_id):
   
  
   form=PassuserForm()

   #Requête de vérification de l'utilisateur
   user_pass=User.query.filter_by(id=user_id).first()
   #Titre
   title='Utilisateur | {}'.format(user_pass.prenom)

   user_nom=user_pass.prenom

   #Autorisation personnelle
   if current_user.id!= user_statu.id:
      return redirect(url_for('user.liuser'))

   if user_pass is None:
      return redirect(url_for('user.liuser'))

   if form.validate_on_submit():
      password_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user_pass.password=password_hash
      db.session.commit()
      return redirect(url_for('auth.logout')) 

   return render_template('user/password.html', form=form, title=title, user_nom=user_nom)


""" Modification des informations de l'utilisateur """

@user.route('/editut_<int:user_id>', methods=['GET', 'POST'])
#@login_required
def edituser(user_id):
       
   form=EditeruserForm()
   
   #Requête de vérification de l'utilisateur
   user_pass=User.query.filter_by(id=user_id).first()
   #Le nom de l'utilisateur en cours de modification
   user_nom=user_pass.prenom
   #Titre
   title='Utilisateur | {}'.format(user_nom)

   if user_pass is None:
      return redirect(url_for('user.liuser'))
   
   #La modification des informations de l'utilisateur.
   if current_user.id is not user_pass.id or current_user.role !='Admin':
      return redirect(url_for('main.dashboard'))

   if form.validate_on_submit():
      if form.ed_username.data == user_pass.username:
         user_pass.nom=form.ed_nom.data.upper()
         user_pass.post_nom=form.ed_post_nom.data.upper()
         user_pass.prenom=form.ed_prenom.data.capitalize()
         user_pass.role=form.ed_role.data
         db.session.commit()
         flash("Modification réussie",'success')
         return redirect(url_for('user.liuser')) 
      else:
         user_pass.nom=form.ed_nom.data.upper()
         user_pass.post_nom=form.ed_post_nom.data.upper()
         user_pass.prenom=form.ed_prenom.data.capitalize()
         user_pass.role=form.ed_role.data
         user_pass.username=form.ed_username.data
         db.session.commit()
         flash("Modification réussie",'success')
         return redirect(url_for('user.liuser')) 
   
   if request.method=='GET':
      form.ed_nom.data=user_pass.nom
      form.ed_post_nom.data=user_pass.post_nom
      form.ed_prenom.data=user_pass.prenom
      form.ed_role.data=user_pass.role
      form.ed_username.data=user_pass.username

   return render_template('user/edituser.html', form=form, title=title, user_nom=user_nom)