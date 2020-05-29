"""
------------------------------------------ Imports ------------------------------------------
"""
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user

from radzblog import db
from radzblog.blogs.forms import CreateBlogForm
from radzblog.comments.forms import CommentForm
from radzblog.models import BlogPost, Comment


"""
----------------------------------------- Blueprint -----------------------------------------
"""
blogs = Blueprint('blogs', __name__)


"""
------------------------------------------- Views -------------------------------------------
"""
@blogs.route('/blogcreate', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateBlogForm()

    if form.validate_on_submit():
        blog = BlogPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('blogs.publish'))

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")
        
        return render_template('createblog.html', form=form)


@blogs.route('/blogcreate/post', methods=['GET', 'POST'])
@login_required
def newpost():
    form = CreateBlogForm()

    if form.validate_on_submit():
        dt = datetime.now()

        blog = BlogPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        blog.written_on = dt
        blog.posted = True
        blog.posted_on = dt

        db.session.add(blog)
        db.session.commit()

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")

    return redirect(url_for('core.home'))


@blogs.route('/blogpublish')
@login_required
def publish():
    posts = BlogPost.query.filter_by(posted=False,user_id=current_user.id).all()
    return render_template('publish.html', posts=posts)

@blogs.route('/blogdetail/<int:id>')
def blogdetail(id):
    blog = BlogPost.query.get_or_404(id)

    if blog.posted:
        form = CommentForm()
        comments = Comment.query.filter_by(postid=id).all()

        return render_template('blogdetail.html', blog=blog, form=form, comments=comments)

    else:
        abort(404)


@blogs.route('/blogpost/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    blog = BlogPost.query.get_or_404(id)

    if blog.author == current_user:
        blog.posted = True
        blog.posted_on = datetime.now()

        db.session.commit()
        return redirect(url_for('core.home'))

    else:
        abort(403)


@blogs.route('/blogedit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    blog = BlogPost.query.get_or_404(id)

    if blog.author == current_user:
        form = CreateBlogForm()

        form.title.data = blog.title
        form.content.data = blog.content

        return render_template('edit.html', form=form, blog=blog)

    else:
        abort(403)


@blogs.route('/blogupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = CreateBlogForm()

    if form.validate_on_submit():
        blog = BlogPost.query.get_pr_404(id)
        
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()

        if blog.posted:
            return redirect(url_for('core.home'))
        else:
            return redirect(url_for('blogs.publish'))

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")
                
        return redirect(url_for('blogs.edit', id=id))


@blogs.route('/blogeditpost/<int:id>', methods=['GET', 'POST'])
@login_required
def editpost(id):
    form = CreateBlogForm()

    if form.validate_on_submit():
        blog = BlogPost.query.get_or_404(id)
        
        blog.title = form.title.data
        blog.content = form.content.data
        blog.posted = True
        blog.posted_on = datetime.now()
        db.session.commit()

        return redirect(url_for('core.home'))

    else:
        for field in form.errors:
            if field != "csrf_token":
                for error in form.errors[field]:
                    flash(error, "danger")
                
        return redirect(url_for('blogs.edit', id=id))


@blogs.route('/blogdelete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = BlogPost.query.get_or_404(id)

    if blog.author == current_user:
        db.session.delete(blog)
        db.session.commit()

        flash(u"Successfully deleted blog post!", "success")

        return redirect(url_for('core.home'))

    else:
        abort(403)