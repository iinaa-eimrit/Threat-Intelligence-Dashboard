import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
mongo_client = None
mongo_db = None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Integrate CORS and Limiter
    from .extensions import configure_extensions
    configure_extensions(app)

    global mongo_client, mongo_db
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    mongo_db = mongo_client.get_default_database()

    # Import blueprints after db and mongo setup to avoid circular imports
    from .routes import api_bp
    from .rules_routes import rules_bp
    from .auth_routes import auth_bp
    from .swaggerui import swaggerui_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(rules_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(swaggerui_bp, url_prefix='/docs')

    # Serve React frontend (built files from frontend/dist)
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'dist')

    @app.route('/')
    def serve_dashboard():
        return send_from_directory(frontend_dist, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        file_path = os.path.join(frontend_dist, path)
        if os.path.isfile(file_path):
            return send_from_directory(frontend_dist, path)
        return send_from_directory(frontend_dist, 'index.html')

    return app
