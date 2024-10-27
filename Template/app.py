from flask_migrate import Migrate
from user_routes import user_blueprint
from recipe_routes import recipe_blueprint
from tag_routes import tag_blueprint
from reviews_routes import review_blueprint
from models import app, db

migrate = Migrate(app, db)

app.register_blueprint(user_blueprint)  
app.register_blueprint(recipe_blueprint)  
app.register_blueprint(tag_blueprint)  
app.register_blueprint(review_blueprint)  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)  