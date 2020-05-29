"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
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
@comments.route('/commentcreate/<int:postid>', methods=['GET', 'POST'])
@login_required
def create(postid):
    form = CommentForm()

    if form.validate_on_submit:
        if form.comment.data:
            comment = Comment(form.comment.data, current_user.id, postid)
            db.session.add(comment)
            db.session.commit()

            flash(u"Comment sent for Approval to admin. It will appear in comments once approved.", "success")

        else:
            abort(404)

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

    return redirect(url_for('blogs.blogdetail', id=postid))


@comments.route('/commentdelete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    comment = Comment.query.get_or_404(id)

    if comment.user == current_user:
        postid = comment.postid

        db.session.delete(comment)
        db.session.commit()

        flash(u"Comment deleted.", "success")
        return redirect(url_for('blogs.blogdetail', id=postid))

    else:
        abort(403)


@comments.route('/commentedit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    comment = Comment.query.get_or_404(id)

    if comment.user == current_user and not comment.approved:
        if request.form.get('edt-comment'):
            comment.comment = request.form.get('edt-comment')
            db.session.commit()

            flash(u"Comment edited.", "success")

        else:
            flash(u"Nothing edited in your unapproved comment.", "warning")

        return redirect(url_for('blogs.blogdetail', id=comment.postid))

    else:
        abort(403)


@comments.route('/admin/approval-list')
@login_required
def adminlist():
    if current_user == "admin":
        comments = Comment.query.filter_by(approved=False).all()
        posts = []

        for comment in comments:
            posts.append(comment.post)
            posts = list(set(posts))

        return render_template('approval-list.html', posts=posts)

    else:
        abort(403)


@comments.route('/commentapprove/<int:id>', methods=['GET', 'POST'])
@login_required
def approve(id):
    comment = Comment.query.get_or_404(id)
    
    if current_user == "admin":
        comment.approved = True
        db.session.commit()

        comments_left = Comment.query.filter_by(postid=comment.postid, approved=False).all()
        flash(u"Comment approved.", "success")

        if comments_left:
            return redirect(url_for('blogs.blogdetail', id=comment.postid))
        else:
            return redirect(url_for('comments.adminlist'))

    else:
        abort(403)