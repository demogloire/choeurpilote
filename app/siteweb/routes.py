from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Article, Categorie, Statpage, Media, Partition 
from app.siteweb.utilities import nosimage
from app.siteweb.forms import AlbumForm, PartForm
from flask_login import login_user, current_user, logout_user, login_required
from . import siteweb

@siteweb.route('/', methods=['GET', 'POST'])
def index():
   title='Bienvenue'
   
   #Triage selon les articles
   cat_id=Categorie.query.filter_by(nom='Article').first()

   ver_post=None
   recent_pub={}
   comm_id={}
   recent_communiqu={}
   nos_images=nosimage()

   if cat_id is not None:
      recent_pub=Article.query.filter_by(statut=True, categorie_id=cat_id.id).order_by(Article.id.desc()).limit(3)
      #Triage selon les communiquées
      comm_id=Categorie.query.filter_by(nom='Communiqué').first()
      recent_communiqu=Article.query.filter_by(statut=True, categorie_id=comm_id.id).all()
      #image de pieds de page
      ver_post="Novide"
   else:
      ver_post="Vide"
     
   return render_template('siteweb/index.html',nos_images=nos_images, ver_post=ver_post, title=title, rec=recent_pub, recm=recent_communiqu)

@siteweb.route('/quisommes-nous.html', methods=['GET', 'POST'])
def quisommes():
   title='Qui sommes-nous?'
   #Page
   page='Qui sommes-nous?'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Apropos
   apropos='apropos'
   nos_images=nosimage()
   
   return render_template('siteweb/apropos/quisommes.html', nos_images=nos_images, apropos=apropos, title=title, rec=qui_id)


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
   nos_images=nosimage()

   return render_template('siteweb/apropos/historique.html',nos_images=nos_images, apropos=apropos, title=title, rec=qui_id)

@siteweb.route('/perspectives.html', methods=['GET', 'POST'])
def prospectif():
   #Page
   page='Perspectives'
   #Triage selon les articles
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Titre de la page
   title=qui_id.titre
   #Apropos
   apropos='apropos'
   nos_images=nosimage()

   return render_template('siteweb/apropos/prospectif.html', nos_images=nos_images, apropos=apropos, title=title, rec=qui_id)

@siteweb.route('/comiteduchoeur.html', methods=['GET', 'POST'])
def comite():
   #Titre de la page
   title='Le comité du choeur'
   page='Comité du choeur'
   qui_id=Statpage.query.filter_by(titre=page).first_or_404()
   #Apropos
   apropos='apropos'
   nos_images=nosimage()
   return render_template('siteweb/apropos/comite.html', nos_images=nos_images, rec=qui_id, apropos=apropos, title=title)


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
   nos_images=nosimage()
   return render_template('siteweb/otherpage/agenda.html',nos_images=nos_images, apropos=apropos, title=title, rec=qui_id)



@siteweb.route('/galerie.html', methods=['GET', 'POST'])
def galerie():
   
   form=AlbumForm()
   #Variable de vérification des informations
   var_photo=None
   #Liste des id
   br_img=[]
   nbr_ulplod=None
   if form.validate_on_submit():
      images=Media.query.filter_by(album_id=form.cate_pub.data.id).order_by(Media.id.desc()).all()
      
      for nbrmedi in images:
         i=nbrmedi.id
         br_img.insert(0,i)
      nbr_ulplod=len(br_img)

      if nbr_ulplod == 0:
         var_photo='Vide'
         print(images)
         flash("Cet album ({}) est vide".format(form.cate_pub.data.nom),'danger')
   else:
      #Triage selon les images
      images=Media.query.order_by(Media.id.desc()).limit(9)
          
   #Titre de la page
   title='Galerie'
   #Apropos
   apropos='apropos'
   rec={'titre':'Galerie', 'page':'Nos images'}
   nos_images=nosimage()
   return render_template('siteweb/otherpage/gellery.html', var_photo=var_photo, form=form, nos_images=nos_images, lesimages=images, title=title, rec=rec)



@siteweb.route('/partition.html', methods=['GET', 'POST'])
def partition():
   #Formulaire des informades partitions    
   form=PartForm()
   #Titre de la page
   title='Partition musicale'

   #Les informations de la partitions sur la plateforme
   page= request.args.get('page', 1, type=int)
   pub_page=Partition.query.filter_by(statut=True).order_by(Partition.id.asc()).paginate(page=page, per_page=50)

   nonmbre=None #Nombre de partition trouvé
   nbr_part=None #Variable de verification
   tpart=[] #Liste des à remplir

   #Les partitions les plus télécharger
   plus_telecharger=Partition.query.filter(Partition.nbr_download >=10).limit(10)


   #Envoie des information depuis le formaulire
   if form.validate_on_submit():
      #Requete partition = 1 Compositeur=0 et Type= 0
      if form.partition.data is not None and form.user_comp.data is None and form.types_part.data is None:
         pub_page=Partition.query.filter_by(statut=True, id=form.partition.data.id)\
         .order_by(Partition.id.asc()).paginate(page=page, per_page=50)
         #Boucle de remplissage du nombre de partition
         for nbrpart in pub_page.items():
            i=nbrpart.id
            tpart.insert(0,i)
         nonmbre=len(tpart)
         #Vérification du nombre de
         if nonmbre == 0:
            nbr_part='Vide'
            flash("Aucune partition prouvée",'danger')
      
      elif form.partition.data is None and form.user_comp.data is not None and form.types_part.data is None:
         pub_page=Partition.query.filter_by(statut=True, user_id=form.user_comp.data.id)\
            .order_by(Partition.id.asc()).paginate(page=page, per_page=50)
            #Boucle de remplissage du nombre de partition
         for nbrpart in pub_page.items:
            i=nbrpart.id
            tpart.insert(0,i)
         nonmbre=len(tpart)
            #Vérification du nombre de
         if nonmbre == 0:
            nbr_part='Vide'
            flash("Aucune partition prouvée",'danger')  

      elif form.partition.data is None and form.user_comp.data is None and form.types_part.data is not None:
         pub_page=Partition.query.filter_by(statut=True, type_id=form.types_part.data.id)\
            .order_by(Partition.id.asc()).paginate(page=page, per_page=50)
            #Boucle de remplissage du nombre de partition
         for nbrpart in pub_page.items:
            i=nbrpart.id
            tpart.insert(0,i)
         nonmbre=len(tpart)
            #Vérification du nombre de
         if nonmbre == 0:
            nbr_part='Vide'
            flash("Aucune partition prouvée",'danger')

      elif form.partition.data is not None and form.user_comp.data is not None and form.types_part.data is None:
         
         pub_page=Partition.query.filter_by(statut=True, user_id=form.user_comp.data.id, id=form.partition.data.id)\
            .order_by(Partition.id.asc()).paginate(page=page, per_page=50)
            #Boucle de remplissage du nombre de partition
         for nbrpart in pub_page.items:
            i=nbrpart.id
            tpart.insert(0,i)
         nonmbre=len(tpart)
            #Vérification du nombre de
         if nonmbre == 0:
            nbr_part='Vide'
            flash("Aucune partition prouvée",'danger')

      elif form.partition.data is None and form.user_comp.data is not None and form.types_part.data is not None:
         pub_page=Partition.query.filter_by(statut=True, user_id=form.user_comp.data.id, type_id=form.types_part.data.id)\
            .order_by(Partition.id.asc()).paginate(page=page, per_page=50)
            #Boucle de remplissage du nombre de partition
         for nbrpart in pub_page.items:
            i=nbrpart.id
            tpart.insert(0,i)
         nonmbre=len(tpart)
            #Vérification du nombre de
         if nonmbre == 0:
            nbr_part='Vide'
            flash("Aucune partition prouvée",'danger')
      else:
         pass

   rec={'titre':'Partitions musicales', 'page':'Nos partitions'}
   nos_images=nosimage()

   #Requet des pagination et des listage des données

   return render_template('siteweb/otherpage/partition.html',nbr_part=nbr_part, plus_telecharger=plus_telecharger, form=form,nos_images=nos_images, partitions=pub_page,rec=rec, title=title )


@siteweb.route('/telech<int:part_id>gement', methods=['GET', 'POST'])
def telecharger(part_id):   
   #Titre
   title='Partition de la messe | Choeur Pilote'
   #Requête de vérification de la partition
   part_li=Partition.query.filter_by(id=part_id).first_or_404()
   #Partition
   nbr_download=None
   if part_li :
      nbr_download=int(part_li.nbr_download)+1
      part_li.nbr_download=nbr_download
      db.session.commit()
      return redirect(part_li.pdf_url)
   return redirect(url_for('siteweb.partition'))



@siteweb.route('/actualite.html', methods=['GET', 'POST'])
def actualite():
   title="Actualité | Choeur pilote"


   #Triage selon les articles
   cat_id=Categorie.query.filter_by(nom='Article').first()

   ver_post=None
   plus_telecharger={}
   pub_page={}
   plus_artic={}
   nos_images=nosimage()

   if cat_id is not None:
      #Requet des pagination et des listage des données
      page= request.args.get('page', 1, type=int)
      pub_page=Article.query.filter_by(statut=True, categorie_id=cat_id.id).order_by(Article.id.asc()).paginate(page=page, per_page=5)

      #Les partitions les precement mise en ligne
      plus_telecharger=Partition.query.filter_by(statut=True).order_by(Partition.id.asc()).limit(10)

      #Les partitions plus populaire
      plus_artic=Article.query.filter(Article.nbr_lecture >=5).limit(5)
      
      ver_post="Novide"
   else:
      ver_post="Vide"
      


   rec={'titre':'News', 'page':'Actualité'}
   return render_template('siteweb/otherpage/actualite.html',plus_artic=plus_artic, ver_post=ver_post, rec=rec, title=title, plus_telecharger=plus_telecharger, nos_images=nos_images, liste=pub_page)



@siteweb.route('/actualite/<int:post_id>/<string:slug_id>.html', methods=['GET', 'POST'])
def postactualite(slug_id,post_id):
   title="Actualité | Choeur pilote"
   actualite=Article.query.filter_by(slug=slug_id, id=post_id).first_or_404()

   nombre=None
   #Initialisation de nombre de vue
   if actualite.nbr_lecture is None:
      nombre=0
   elif actualite.nbr_lecture == 0:
      nombre=int(actualite.nbr_lecture)+1
   elif actualite.nbr_lecture:
      nombre=int(actualite.nbr_lecture)+1
      
   #Mise à jour de la base des données
   actualite.nbr_lecture=nombre
   db.session.commit()
   
   #Les partitions les precement mise en ligne
   plus_telecharger=Partition.query.filter_by(statut=True).order_by(Partition.id.asc()).limit(10)

   #Les partitions plus populaire
   plus_artic=Article.query.filter(Article.nbr_lecture >=5).limit(5)

   nos_images=nosimage()
   rec={'titre':'News', 'page':'Actualité'}
   return render_template('siteweb/otherpage/article.html',plus_artic=plus_artic, rec=rec, title=title, plus_telecharger=plus_telecharger, nos_images=nos_images, actualite=actualite)



@siteweb.route('/contact.html', methods=['GET', 'POST'])
def contact():
   title="Contactez - nous | Choeur pilote"

   #Les partitions les precement mise en ligne
   plus_telecharger=Partition.query.filter_by(statut=True).order_by(Partition.id.asc()).limit(10)
   #Les partitions plus populaire
   plus_artic=Article.query.filter(Article.nbr_lecture >=5).limit(5)
   nos_images=nosimage()
   rec={'titre':'Contactez-nous', 'page':'Nos coordonées'}
   return render_template('siteweb/otherpage/contact.html',plus_artic=plus_artic, rec=rec, title=title, plus_telecharger=plus_telecharger, nos_images=nos_images)
