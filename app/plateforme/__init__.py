from flask import Blueprint

plateforme = Blueprint('plateforme', __name__, url_prefix='/')
# never forget 
from . import routes