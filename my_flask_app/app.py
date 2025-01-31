import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from models import db  # Import the 'db' instance from models
from resources.recipe import RecipeResource
from resources.review import ReviewResource
from resources.user import UserResource
from resources.login import LoginResource  # Ensure 'login' is lowercase


# Initialize extensions (db is already initialized in models)
def create_app():
    app = Flask(__name__)

    # Use environment variable for the database URI (Optional, recommended for production)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)

    # Define routes
    @app.route('/')
    def home():
        return "Welcome to the Recipe Sharing API"

    # Add resources to API
    api.add_resource(RecipeResource, '/recipes', '/recipes/<int:recipe_id>')
    api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(LoginResource, '/login')  # Add the login route

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    
    # Ensure the app is in the app context to create tables if needed
    with app.app_context():
        db.create_all()  # Create database tables
        print("Database tables created!")
    
    app.run(debug=True)
