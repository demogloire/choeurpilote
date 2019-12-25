from flask import Blueprint

statpage = Blueprint('statpage', __name__, url_prefix='/pages')
# never forget 
from . import routes