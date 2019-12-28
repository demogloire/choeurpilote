from flask import render_template, flash, url_for, redirect, request, session
from ..models import Media 

def nosimage():
    liste_all=Media.query.order_by(Media.id.desc()).limit(8)
    return liste_all
