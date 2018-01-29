from flask import jsonify
from app.exceptions import ValidationError
from .import  api

def forbidden(message):
	response=jsonify({'error':'forbidden','message':message})
	response.status_code=403
	return response

def bad_request(message):
	response=jsonify({'error':'bad_request','message':message})
	response.status_code=400
	return response

def unauthorized(message):
	response=jsonify({'error':'unauthorized','message':message})
	response.status_code=401
	return response

def not_found(message):
	response=jsonify({'error':'not_found','message':message})
	response.status_code=404
	return response

def method_not_allowed(message):
	response=jsonify({'error':'method_not_allowed','message':message})
	response.status_code=405
	return response

def internal_server_error(message):
	response=jsonify({'error':'internal_server_error','message':message})
	response.status_code=500
	return response
