from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
hostname = os.getenv("HOSTNAME")
database = os.getenv("DATABASE")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
port = os.getenv("PORT_ID")
secret_key = os.getenv("SECURITY")

# Configure SQLAlchemy database connection
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@{hostname}/{database}"
app.config["SECRET_KEY"] = secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Association table for Recipe and Tag (many-to-many relationship)
recipe_tags = db.Table("recipe_tags",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)

# User model
class Users(db.Model):
    """
    Model class representing users in the database.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Store hashed password

    def __init__(self, username, password):
        """
        Initialize a new user object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = hashpw(password.encode("utf-8"), gensalt(9)).decode("utf-8")  # Hash password during initialization

class Recipe(db.Model):
    """
    Model class representing recipes in the database.

    Attributes:
        id (int): The unique identifier for the recipe.
        recipe_name (str): The name of the recipe.
        ingredients (str): The ingredients required for the recipe.
        instructions (str): The instructions to prepare the recipe.
        created_at (datetime): The timestamp when the recipe was created.
        user_id (int): The user ID of the creator of the recipe.
        created_by (str): The username of the creator of the recipe.
        user (relationship): Relationship with the Users model.
        tags (relationship): Relationship with the Tag model.
        recipe_reviews (relationship): Relationship with the Review model.
    """
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("Users", backref=db.backref("recipes", lazy=True, cascade="all, delete-orphan"))
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_by = db.Column(db.String(80), nullable=False)  
    # user = db.relationship("Users", backref=db.backref("recipes", lazy=True)) 
    tags = db.relationship("Tag", secondary=recipe_tags, backref=db.backref("recipes", lazy="dynamic"))
    recipe_reviews = db.relationship("Review", back_populates="recipe")


    def __init__(self, recipe_name, ingredients, instructions, user, created_by, reviews=None, tags=None, created_at=None):
        """
        Initialize a new recipe object.

        Args:
            recipe_name (str): The name of the recipe.
            ingredients (str): The ingredients required for the recipe.
            instructions (str): The instructions to prepare the recipe.
            user (Users): The user who created the recipe.
            created_by (str): The username of the creator of the recipe.
            created_at (datetime, optional): The timestamp when the recipe was created. Defaults to None.
        """
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.user = user
        self.created_by = created_by
        if reviews is None:
            self.reviews = []  # Initialize an empty list for reviews
        else:
            self.reviews = reviews
        self.tags = tags if tags is not None else []
        if created_at is None:
            self.created_at = datetime.utcnow()
        else:
            self.created_at = created_at

    def add_review(self, review):
        self.reviews.append(review)


# Tag model
class Tag(db.Model):
    """
    Model class representing tags in the database.

    Attributes:
        id (int): The unique identifier for the tag.
        tag_name (str): The name of the tag.
    """
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, tag_name):
        """
        Initialize a new tag object.

        Args:
            tag_name (str): The name of the tag.
        """
        self.tag_name = tag_name

class Review(db.Model):
    """
    Model class representing reviews in the database.

    Attributes:
        id (int): The unique identifier for the review.
        review_content (str): The content of the review.
        created_at (datetime): The timestamp when the review was created.
        is_anonymous (bool): Flag indicating if the review is anonymous.
        user_id (int): The user ID of the reviewer.
        recipe_id (int): The recipe ID that the review is associated with.
        recipe_name (str): The name of the recipe that the review is associated with.
        user (relationship): Relationship with the Users model.
        recipe (relationship): Relationship with the Recipe model.
    """
    id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))  # Foreign key to Recipe table
    recipe = db.relationship("Recipe", backref="reviews")  # Establish the relationship


    user = db.relationship("Users", backref=db.backref("reviews", lazy=True))
    recipe = db.relationship("Recipe", backref=db.backref("reviews"))

    def __init__(self, review_content, user_id=None, recipe_id=None, created_at=None, is_anonymous=False):
        """
        Initialize a new review object.

        Args:
            review_content (str): The content of the review.
            user_id (int, optional): The user ID of the reviewer. Defaults to None.
            recipe_id (int, optional): The recipe ID that the review is associated with. Defaults to None.
            created_at (datetime, optional): The timestamp when the review was created. Defaults to None.
            is_anonymous (bool, optional): Flag indicating if the review is anonymous. Defaults to False.
        """
        self.review_content = review_content
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.is_anonymous = is_anonymous