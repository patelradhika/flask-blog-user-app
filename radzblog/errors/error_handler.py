"""
------------------------------------------ Imports ------------------------------------------
"""
from flask import Blueprint,render_template


"""
----------------------------------------- Blueprint -----------------------------------------
"""
error = Blueprint('error', __name__)


"""
------------------------------------------ Handler ------------------------------------------
"""
@error.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'), 404

@error.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'), 403
