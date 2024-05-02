# Importing necessary blueprints and modules
from flask_migrate import Migrate
from user_routes import user_blueprint
from recipe_routes import recipe_blueprint
from tag_routes import tag_blueprint
from reviews_routes import review_blueprint
from Template.models import app, db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Registering blueprints with the Flask app
app.register_blueprint(user_blueprint)  # User-related routes
app.register_blueprint(recipe_blueprint)  # Recipe-related routes
app.register_blueprint(tag_blueprint)  # Tag-related routes
app.register_blueprint(review_blueprint)  # Review-related routes

# Creating database tables if they don't exist and running the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all database tables
    app.run(debug=True)  # Run the Flask app in debug mode