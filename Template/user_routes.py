from flask import Blueprint, jsonify, request
from models import Users, db, app
from bcrypt import checkpw
from functools import wraps
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta

load_dotenv()


user_blueprint = Blueprint("user_blueprint", __name__)

Algorithms = os.getenv("algo_key")
secret_key = os.getenv("SECURITY")

app.config["SECRET_KEY"] = secret_key


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Missing token"}), 401

        if not token.startswith("Bearer "):
            return jsonify({"message": "Invalid token format. Token must start with 'Bearer'"}), 401
        
        available_token = token.split(" ")
        if len(available_token) != 2:
            return jsonify({"message": "Invalid token format. Token must be provided after 'Bearer'"}), 401

        token = available_token[1]

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=[Algorithms])

            user_id = data["user_id"]
            request.user_id = user_id

        except jwt.ExpiredSignatureError:
            print("Token has expired") 
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError as error:
            print(f"Invalid token: {error}")  
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function



@user_blueprint.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify({"message": "Both username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409

    new_user = Users(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "User ID": Users.id}), 201


@user_blueprint.route("/login", methods=["POST"])
def login():
    """Log in a user."""
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = Users.query.filter_by(username=username).first()
    if user and checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        # Create a JWT token with expiry time
        expiry_time = datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
        token = jwt.encode({"user_id": user.id, "exp": expiry_time}, app.config["SECRET_KEY"], algorithm=Algorithms)

        # decoded_token = token.decode("utf-8")

        return jsonify({"message": "Login successful", "token": token, "expires_at": expiry_time}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@user_blueprint.route("/users", methods=["DELETE"])
@token_required
def delete_user(user_id):
    """Delete user"""
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@user_blueprint.route("/logout", methods=["DELETE"])
@token_required
def logout(user_id):
    """Log out the current user."""
    return jsonify({"message": "Logged out successfully"}), 200