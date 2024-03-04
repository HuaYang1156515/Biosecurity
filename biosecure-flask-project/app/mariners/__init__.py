from flask import Blueprint

mariners_blueprint = Blueprint('mariners', __name__)

from . import views
