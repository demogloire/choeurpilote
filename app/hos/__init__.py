from flask import Blueprint

hos = Blueprint('hos', __name__, url_prefix='/hotspot')
# never forget 
from . import routes