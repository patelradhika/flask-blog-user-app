"""
------------------------------------------ Imports ------------------------------------------
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo


"""
------------------------------------------- Forms -------------------------------------------
"""
class RegisterForm(FlaskForm):
    email = EmailField("Email ID", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("check_password", message="Passwords must match!")])
    check_password = PasswordField("Re-enter Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class UpdateForm(FlaskForm):
    email = EmailField("Email ID")
    username = StringField("Username")
    password = PasswordField("Password", validators=[EqualTo("check_password", message="Passwords must match!")])
    check_password = PasswordField("Re-enter Password")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png', 'jpg', 'gif'])])
    submit = SubmitField("Update")