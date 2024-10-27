from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()

hostname = os.getenv("HOSTNAME")
database = os.getenv("DATABASE")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
port = os.getenv("PORT_ID")
secret_key = os.getenv("SECURITY")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@{hostname}/{database}"
app.config["SECRET_KEY"] = secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)

recipe_tags = db.Table("recipe_tags",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) 

    def __init__(self, username, password):
        self.username = username
        self.password = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("Users", backref=db.backref("recipes", lazy=True, cascade="all, delete-orphan"))
    created_by = db.Column(db.String(80), nullable=False)  
    tags = db.relationship("Tag", secondary=recipe_tags, backref=db.backref("recipes", lazy="dynamic"))
    recipe_reviews = db.relationship("Review", back_populates="recipe")


    def __init__(self, recipe_name, ingredients, instructions, user, created_by, reviews=None, tags=None, created_at=None):
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.user = user
        self.created_by = created_by
        if reviews is None:
            self.reviews = [] 
        else:
            self.reviews = reviews
        self.tags = tags if tags is not None else []
        if created_at is None:
            self.created_at = datetime.utcnow()
        else:
            self.created_at = created_at

    def add_review(self, review):
        self.reviews.append(review)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, tag_name):
        self.tag_name = tag_name

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))  
    recipe = db.relationship("Recipe", backref="reviews") 


    user = db.relationship("Users", backref=db.backref("reviews", lazy=True))
    recipe = db.relationship("Recipe", backref=db.backref("reviews"))

    def __init__(self, review_content, user_id=None, recipe_id=None, created_at=None, is_anonymous=False):
        self.review_content = review_content
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.is_anonymous = is_anonymous