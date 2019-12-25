from flask import redirect, session, url_for
from functools import wraps

def upload_acif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        return f(*args, **kwargs)
      else:
        return redirect(url_for('album.ajoutalbm'))
    return wrap

def upload_inactif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        session.pop('album', None)
        return f(*args, **kwargs)
      else:
        return f(*args, **kwargs)
    return wrap