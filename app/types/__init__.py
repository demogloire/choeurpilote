from flask import Blueprint

types = Blueprint('types', __name__, url_prefix='/types')
# never forget 
from . import routes