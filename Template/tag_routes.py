from flask import Blueprint, jsonify, request, session
from Template.models import Tag, db, Recipe, recipe_tags
from functools import wraps

# Creating a Blueprint for tag-related routes
tag_blueprint = Blueprint("tag_blueprint", __name__)


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
            # If user is not logged in, return 401 Unauthorized
            return jsonify({"message": "Please log in to access this"}), 401
        return f(*args, **kwargs)
    return decorated_function


@tag_blueprint.route("/recipes/<int:recipe_id>/tags", methods=["POST"])
@login_required
def create_tag(recipe_id):
    """Create a new tag for a specific recipe."""
    data = request.get_json()
    tag_name = data.get("tag_name")  # Use get method to avoid KeyError
    if not tag_name:
        return jsonify({"message": "Tag name is missing"}), 400

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    # Check if the tag name already exists
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if existing_tag:
        return jsonify({"message": "Tag name already exists"}), 400

    # Create a new tag
    new_tag = Tag(tag_name=tag_name)

    # Associate the new tag with the recipe
    recipe.tags.append(new_tag)

    # Add new tag to database
    db.session.add(new_tag)
    db.session.commit()
    
    # Return success message
    return jsonify({"message": "Tag created successfully"}), 201


@tag_blueprint.route("/tags/<int:tag_id>", methods=["GET"])
@login_required
def get_tag(tag_id):
    """Get details of a specific tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    
    # Get associated recipes for the tag
    associated_recipes = [recipe.recipe_name for recipe in tag.recipes]

    # Construct response data for the tag
    tag_data = {
        "id": tag.id,
        "tag_name": tag.tag_name,
        "associated_recipes": associated_recipes
    }
    # Return tag details
    return jsonify(tag_data), 200



@tag_blueprint.route("/tags/<int:tag_id>", methods=["PUT"])
@login_required
def update_tag(tag_id):
    """Update a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    data = request.get_json()
    tag.tag_name = data["tag_name"]
    # Commit changes to database
    db.session.commit()
    # Return success message
    return jsonify({"message": "Tag updated successfully"}), 200


@tag_blueprint.route("/tags/<int:tag_id>", methods=["DELETE"])
@login_required
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    # Delete tag from database
    db.session.delete(tag)
    db.session.commit()
    # Return success message
    return jsonify({"message": "Tag deleted successfully"}), 200