"""
------------------------------------------ Imports ------------------------------------------
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


"""
------------------------------------------- Forms -------------------------------------------
"""
class CommentForm(FlaskForm):
    comment = TextAreaField("Your thoughts (Comments)", validators=[DataRequired()])
    submit = SubmitField("Publish")