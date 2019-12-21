from datetime import datetime
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article, Wificode 
from app.hos.forms import LoginHostForm
from app.fonction.fonction import setcookie, unix_time
from flask_login import login_user, current_user, logout_user, login_required
from app.hos.utiliescode import usernameString, passwordString, trente_minute, macadress, un_heure, quinze_jours, trente_jours
from . import hos

@hos.route('/listecode', methods=['GET', 'POST'])
@login_required
def hotsgen():
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   title='Code générer'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   pub_page=Wificode.query.order_by(Wificode.id.asc()).paginate(page=page, per_page=100)
  
   return render_template('hos/views.html',  title=title, liste=pub_page)


@hos.route('/ajoutercode', methods=['GET', 'POST'])
@login_required
def hotcode():

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   title='Code générer'
   
   return render_template('hos/conf.html',  title=title)


#Génération de 100 code 3o minutes
@hos.route('/codege', methods=['GET', 'POST'])
@login_required
def hotcodegen():

   title='Code générer'   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   compteur=0
   while compteur < 101:
      code_trente_min=Wificode.query.filter_by(code_username=usernameString()).first()
      if code_trente_min is None:
         ajoutercode=Wificode(code_username=usernameString(), code_password=passwordString(),code_validation='A')
         db.session.add(ajoutercode)
         db.session.commit()
      else:
         pass
      compteur += 1
   
      if compteur == 100:
         flash('100 Codes générés automatiquement','success')
         return redirect(url_for('hos.hotsgen'))

   return render_template('hos/views.html',  title=title)

#Génération de 100 code 1 heures
@hos.route('/codegeun', methods=['GET', 'POST'])
@login_required
def hotcodegenun():

   title='Code générer'   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   compteur=0
   while compteur < 101:
      code_trente_min=Wificode.query.filter_by(code_username=usernameString()).first()
      if code_trente_min is None:
         ajoutercode=Wificode(code_username=usernameString(), code_password=passwordString(),code_validation='B')
         db.session.add(ajoutercode)
         db.session.commit()
      else:
         pass
      compteur += 1
   
      if compteur == 100:
         flash('100 Codes générés automatiquement','success')
         return redirect(url_for('hos.hotsgen'))

   return render_template('hos/views.html',  title=title)

#Génération de 100 code 15jrs
@hos.route('/codegedeux', methods=['GET', 'POST'])
@login_required
def hotcodegendeux():

   title='Code générer'   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   compteur=0
   while compteur < 101:
      code_trente_min=Wificode.query.filter_by(code_username=usernameString()).first()
      if code_trente_min is None:
         ajoutercode=Wificode(code_username=usernameString(), code_password=passwordString(),code_validation='C')
         db.session.add(ajoutercode)
         db.session.commit()
      else:
         pass
      compteur += 1
   
      if compteur == 100:
         flash('100 Codes générés automatiquement','success')
         return redirect(url_for('hos.hotsgen'))

   return render_template('hos/views.html',  title=title)

#Génération de 100 code 30 jours

@hos.route('/codegetrois', methods=['GET', 'POST'])
@login_required
def hotcodegentrois():
       

   title='Code générer'   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   compteur=0
   while compteur < 101:
      code_trente_min=Wificode.query.filter_by(code_username=usernameString()).first()
      if code_trente_min is None:
         ajoutercode=Wificode(code_username=usernameString(), code_password=passwordString(),code_validation='D')
         db.session.add(ajoutercode)
         db.session.commit()
      else:
         pass
      compteur += 1
   
      if compteur == 100:
         flash('100 Codes générés automatiquement','success')
         return redirect(url_for('hos.hotsgen'))

   return render_template('hos/views.html',  title=title)


   
@hos.route('/login', methods=['GET', 'POST'])
def connexion():

   title='Hotspot'

   if 'fin' in session:
      return redirect(url_for('plateforme.index'))
   else:
      pass

   form=LoginHostForm()



   if form.validate_on_submit():
   
      hotspot=Wificode.query.filter_by(code_username=form.code_username.data).first()

      if hotspot is None:
         flash('Verifier vos identifiants','danger')
         return redirect(url_for('hos.connexion'))
      
      #Date
      date_actuelle=datetime.utcnow()

      if hotspot.fin_validation==date_actuelle:
         hotspot.statut=True
         db.session.commit()
         flash('Votre code est déjà perimé','danger')
         return redirect(url_for('hos.connexion'))
         
      if hotspot and hotspot.code_password==form.code_password.data:
         if hotspot.statut==False:
            if hotspot.code_validation=='A':
               temps=trente_minute()
               temps_debut=temps[0]
               temps_fin=temps[1]
               mac_addresse=macadress()
               hotspot.debut_validation=temps_debut
               hotspot.fin_validation=temps_fin
               hotspot.adresse_mac=mac_addresse
               db.session.commit()
               session['fin']=temps_fin
               
               return redirect(url_for('plateforme.index'))
            if hotspot.code_validation=='B':
               temps=un_heure()
               temps_debut=temps[0]
               temps_fin=temps[1]
               mac_addresse=macadress()
               hotspot.debut_validation=temps_debut
               hotspot.fin_validation=temps_fin
               hotspot.adresse_mac=mac_addresse
               db.session.commit()
               session['fin']=temps_fin
               
               return redirect(url_for('plateforme.index'))
            if hotspot.code_validation=='C':
               temps=quinze_jours()
               temps_debut=temps[0]
               temps_fin=temps[1]
               mac_addresse=macadress()
               hotspot.debut_validation=temps_debut
               hotspot.fin_validation=temps_fin
               hotspot.adresse_mac=mac_addresse
               db.session.commit()
               session['fin']=temps_fin
               
               return redirect(url_for('plateforme.index'))
            if hotspot.code_validation=='D':
               temps=trente_jours()
               temps_debut=temps[0]
               temps_fin=temps[1]
               mac_addresse=macadress()
               hotspot.debut_validation=temps_debut
               hotspot.fin_validation=temps_fin
               hotspot.adresse_mac=mac_addresse
               db.session.commit()
               session['fin']=temps_fin
               setcookie(valeur=str(temps_fin),temps=temps_fin)
               return redirect(url_for('plateforme.index'))
         else:
            mac_addresse=macadress()
            if mac_addresse==hotspot.adresse_mac:
               return redirect(url_for('plateforme.index'))
            else:
               flash('Code ne pas lié à cet équipement','danger')
               return redirect(url_for('hos.connexion'))    
      else:
         flash('Verifier vos identifiants','danger')
         return redirect(url_for('hos.connexion'))
             
            
         

   return render_template('hos/omb.html', form=form, title=title)