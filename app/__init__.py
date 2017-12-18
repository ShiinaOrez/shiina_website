def create_app(config_name):
	from version_1.0 import api as api_1.0_blueprint
	app.register_blueprint(api_1.0_blueprint,url_prefix='/shiina_website/v1.0')
