import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
#from wtf_tinymce import wtf_tinymce
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown

#Importation des configuration de l'application sur le developpement de l'application
from config import app_config



db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

#Structure de l'application

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config.from_mapping(
        CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL') or 'Pegue a sua Key',
    )


    #Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Markdown(app)
    migrate = Migrate(app, db)
    #wtf_tinymce.init_app(app)
    

    login_manager.login_message = "Veuillez vous connecté"
    login_manager.login_view = "auth.login"
    login_manager.login_message_category ='danger'
    #SimpleMDE(app)

    #md= Markdown(app, extensions=['fenced_code'])
    from app import models

    ''' 
    Utilisation des stucture Blueprint
    '''

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .authentification import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import user as main_user
    app.register_blueprint(main_user)

    from .categorie import categorie as categorie_blueprint
    app.register_blueprint(categorie_blueprint)

    from .publication import publication as publication_blueprint
    app.register_blueprint(publication_blueprint)

    from .types import types as types_blueprint
    app.register_blueprint(types_blueprint)

    from .partition import partition as partition_blueprint
    app.register_blueprint(partition_blueprint)

    from .siteweb import siteweb as siteweb_blueprint
    app.register_blueprint(siteweb_blueprint)

    return app
