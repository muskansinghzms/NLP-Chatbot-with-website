import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import shared database instance
from database import db

# Initialize Flask-Login
login_manager = LoginManager()

def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Configure app
    app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
    
    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'ecommerce.db')}"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Enable CORS
    CORS(app)

    # Import routes after app creation to avoid circular imports
    with app.app_context():
        # Import models to ensure they're registered with the ORM
        import models
        
        # Create all tables
        db.create_all()
        
        # Register blueprints
        from app import main_bp, auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        
    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
