"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import render_template, Blueprint

from radzblog.models import BlogPost


"""
----------------------------------------- Blueprint -----------------------------------------
"""
core = Blueprint('core', __name__)


"""
------------------------------------------- Views -------------------------------------------
"""
@core.route('/')
def home():
    blogs = BlogPost.query.filter_by(posted=True).all()
    return render_template('home.html', blogs=blogs)


@core.route('/about')
def about():
    return render_template('about.html')