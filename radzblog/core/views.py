"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import render_template, Blueprint, request

from radzblog.models import BlogPost


"""
----------------------------------------- Blueprint -----------------------------------------
"""
core = Blueprint('core', __name__)


"""
------------------------------------------- Views -------------------------------------------
"""
@core.route('/', defaults={"page": 1})
@core.route('/<int:page>')
def home(page):
    blogs = BlogPost.query.filter_by(posted=True).order_by(BlogPost.posted_on.desc()).paginate(page=page, per_page=2, error_out=False)
    return render_template('home.html', blogs=blogs)


@core.route('/about')
def about():
    return render_template('about.html')