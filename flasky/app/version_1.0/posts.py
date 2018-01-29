from flask import jsonify,request,g,url_for,current_app
from .. import db
from ..models import Text,Permission
from . import api
from .decorators import permission_required
from .errors import forbidden

@api.route('/posts/')
def get_posts():
	page=request.args.get('page')
