from flask import Blueprint

siteweb = Blueprint('siteweb', __name__, url_prefix='/')
# never forget 
from . import routes