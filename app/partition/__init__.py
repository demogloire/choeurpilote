from flask import Blueprint

partition = Blueprint('partition', __name__, url_prefix='/partition')
# never forget 
from . import routes