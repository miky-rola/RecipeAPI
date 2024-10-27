from flask import (
    Blueprint, 
    jsonify, 
    request
)
from models import Tag, db, Recipe
from user_routes import token_required

tag_blueprint = Blueprint("tag_blueprint", __name__)



@tag_blueprint.route("/recipes/<int:recipe_id>/tags", methods=["POST"])
@token_required
def create_tag(recipe_id):
    """Create a new tag for a specific recipe."""
    data = request.get_json()
    tag_name = data.get("tag_name")  
    if not tag_name:
        return jsonify({"message": "Tag name is missing"}), 400

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if existing_tag:
        return jsonify({"message": "Tag name already exists"}), 400

    new_tag = Tag(tag_name=tag_name)

    recipe.tags.append(new_tag)

    db.session.add(new_tag)
    db.session.commit()
    
    return jsonify({"message": "Tag created successfully"}), 201


@tag_blueprint.route("/tags/<int:tag_id>", methods=["GET"])
@token_required
def get_tag(tag_id):
    """Get details of a specific tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    
    associated_recipes = [recipe.recipe_name for recipe in tag.recipes]

    tag_data = {
        "id": tag.id,
        "tag_name": tag.tag_name,
        "associated_recipes": associated_recipes
    }
    return jsonify(tag_data), 200



@tag_blueprint.route("/tags/<int:tag_id>", methods=["PUT"])
@token_required
def update_tag(tag_id):
    """Update a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    data = request.get_json()
    tag.tag_name = data["tag_name"]
    db.session.commit()
    return jsonify({"message": "Tag updated successfully"}), 200


@tag_blueprint.route("/tags/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted successfully"}), 200