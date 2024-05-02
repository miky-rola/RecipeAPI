from flask import Blueprint, jsonify, request, session
from Template.models import Users, db
from bcrypt import checkpw
from functools import wraps

# Creating a Blueprint for user-related routes
user_blueprint = Blueprint("user_blueprint", __name__)

def login_required(f):
    """
    Decorator function to check if the user is logged in.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"message": "Please log in to access this"}), 401
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

    # Creating a new user in the database
    new_user = Users(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    # Return the user_id in the response
    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201


@user_blueprint.route("/login", methods=["POST"])
def login():
    """Log in a user."""
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = Users.query.filter_by(username=username).first()
    if user and checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        session["user_id"] = user.id  # Store user_id in session
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@user_blueprint.route("/users", methods=["DELETE"])
@login_required
def delete_user():
    """Delete user"""
    user_id = session["user_id"]
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    session.pop("user_id", None)
    return jsonify({"message": "User deleted successfully"}), 200


@user_blueprint.route("/logout", methods=["DELETE"])
@login_required
def logout():
    """Log out the current user."""
    session.pop("user_id", None)  # Remove user_id from the session
    return jsonify({"message": "Logged out successfully"}), 200
