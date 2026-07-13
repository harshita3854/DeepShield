from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
import os

from extensions import db, bcrypt, login_manager

from routes.image import image_bp
from routes.text import text_bp
from routes.summarizer import summarizer_bp
from routes.paraphraser import paraphraser_bp
from routes.grammar import grammar_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'deepshield-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)  # Enable CORS for frontend integration
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Configure upload folder
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Register Blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(image_bp, url_prefix='/image')
    app.register_blueprint(text_bp, url_prefix='/text')
    app.register_blueprint(summarizer_bp, url_prefix='/summarize')
    app.register_blueprint(paraphraser_bp, url_prefix='/paraphrase')
    app.register_blueprint(grammar_bp, url_prefix='/grammar')
    
    @app.route('/')
    def index():
        return render_template('index.html', current_user=current_user)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
