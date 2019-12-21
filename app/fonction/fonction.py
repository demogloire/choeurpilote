import uuid
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta, MO
from flask import render_template, flash, url_for, redirect, request, session, make_response





# def mydecorator(msg="Hello"):
#     def decorated(f):
#         def wrapper(*args, **kwargs):

#             print("voir message est:" +msg)
#             print("Avant")
#             f(*args, **kwargs)
#             print("Apres")
#         return wrapper
#     return decorated

''' Décoration cookies '''

def mydeclogin(f):
    def wrapper(*args, **kwargs):
        if 'fin' in session:
            return redirect(url_for('hos.connexion'))
        else:
            return redirect(url_for('hos.connexion'))
        f(*args, **kwargs)
    return wrapper


''' convertsion en total_seconds '''

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

#Envoie de cookie
def setcookie(valeur=None,temps=None):
    res= make_response('Cookie')
    res.set_cookie(
        b'df', 
        value=valeur, 
        max_age=None, 
        expires=temps, 
        path='/', 
        domain=None, 
        secure=False, 
        httponly=False, 
        samesite=None
        )
    return res
    
#Réception des cookies
def getcookie():
    res= request.cookies.get('df')
    return res

def login_session():
    if 'fin' in session:
        pass
    else:
        return redirect(url_for('hos.connexion'))

    return redirect(url_for('hos.connexion'))