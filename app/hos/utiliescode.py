import random
import string
import time
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO

#Pour générer un username 
def usernameString(length=4):
    #put your letters in the following string
    your_letters='abcdefghijklmnoprstqvwxyz0123456789'
    return ''.join((random.choice(your_letters) for i in range(length)))

#Pour générer un mot de passe
def passwordString(length=6):
    #put your letters in the following string
    your_letters='abcdefghijklmnoprstqvwxyz0123456789@'
    return ''.join((random.choice(your_letters) for i in range(length)))


def trente_minute():
    heure_actuelle=datetime.utcnow()
    validite_trente= heure_actuelle+ relativedelta(minutes=+30)
    validite_actuelle=(heure_actuelle,validite_trente)
    return validite_actuelle

def un_heure():
    heure_actuelle=datetime.utcnow()
    temps= heure_actuelle+ relativedelta(hours=+1)
    validite_actuelle=(heure_actuelle,temps)
    return validite_actuelle

def quinze_jours():
    heure_actuelle=datetime.utcnow()
    temps= heure_actuelle+ relativedelta(day=+15)
    validite_actuelle=(heure_actuelle,temps)
    return validite_actuelle

def trente_jours():
    heure_actuelle=datetime.utcnow()
    temps= heure_actuelle+ relativedelta(day=+30)
    validite_actuelle=(heure_actuelle,temps)
    return validite_actuelle

def macadress():
    var=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return var

