"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user

from radzblog import db
from radzblog.comments.forms import CommentForm
from radzblog.models import Comment


"""
----------------------------------------- Blueprint -----------------------------------------
"""
comments = Blueprint('comments', __name__)


"""
------------------------------------------- Views -------------------------------------------
"""
@comments.route('/commentcreate/<int:postid>', methods=['POST'])
@login_required
def create(postid):
    form = CommentForm()

    if form.validate_on_submit:
        comment = Comment(form.comment.data, current_user.id, postid)
        db.session.add(comment)
        db.session.commit()

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

    return redirect(url_for('blogs.blogdetail', id=postid))


@comments.route('/commentdelete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    comment = Comment.query.get(id)
    postid = comment.postid

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('blogs.blogdetail', id=postid))


@comments.route('/commentedit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    comment = Comment.query.get(id)

    comment.comment = request.form.get('edt-comment')
    db.session.commit()

    return redirect(url_for('blogs.blogdetail', id=comment.postid))