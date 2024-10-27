from flask import (
    Blueprint, 
    jsonify, 
    request
)
from sqlalchemy import or_
from models import (
    Recipe, 
    db, 
    Tag, 
    Users,
    Review
)
from user_routes import token_required

recipe_blueprint = Blueprint("recipe_blueprint", __name__)


@recipe_blueprint.route("/recipes/create", methods=["POST"])
@token_required
def create_recipe():
    try:
        data = request.get_json()

        recipe_name = data.get("recipe_name")
        ingredients = data.get("ingredients")
        instructions = data.get("instructions")
        
        if not (recipe_name and ingredients and instructions):
            return jsonify({"message": "Missing required fields"}), 400

        user_id = request.user_id

        user = Users.query.get(user_id)
        created_by = user.username
        
        tags_data = data.get("tags", [])
        tags = []
        for tag_info in tags_data:
            tag_name = tag_info.get("tag_name")
            if tag_name:
                tag = Tag.query.filter_by(tag_name=tag_name).first()
                if not tag:
                    tag = Tag(tag_name=tag_name)
                tags.append(tag)

        reviews_data = data.get("reviews", [])
        reviews = [Review(review_content=review.get("content"), user=user) for review in reviews_data]

        new_recipe = Recipe(
            recipe_name=recipe_name,
            ingredients=ingredients,
            instructions=instructions,
            user=user,
            created_by=created_by,
            reviews=reviews,
            tags=tags
        )

        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({"message": "Recipe created successfully", "recipe_id": new_recipe.id}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": "An error occurred while creating the recipe"}), 500



@recipe_blueprint.route("/recipes", methods=["GET"])
@token_required
def get_all_recipes():
    """Get all recipes or search for recipes by name."""
    search_term = request.args.get("search", "")
    specific_name = request.args.get("name")
    
    if specific_name and search_term:
        return jsonify({"error": "Please provide only one of 'search' or 'name' parameters."}), 400

    if specific_name:
        recipes = Recipe.query.filter(Recipe.recipe_name.ilike(f"%{specific_name}%")).all()
    elif search_term:
        recipes = Recipe.query.filter(
            or_(
                Recipe.recipe_name.ilike(f"%{search_term}%"),
                Recipe.ingredients.ilike(f"%{search_term}%"),
                Recipe.tags.any(Tag.tag_name.ilike(f"%{search_term}%"))
            )
        ).all()
    else:
        recipes = Recipe.query.all()

    recipes_data = []
    for recipe in recipes:
        recipe_data = {
            "recipe_id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
            "created_at": recipe.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "user": recipe.user.username,
            "reviews": [review.review_content for review in recipe.reviews],
            "tags": [tag.tag_name for tag in recipe.tags]
        }
        recipes_data.append(recipe_data)
    return jsonify({"recipes": recipes_data}), 200



@recipe_blueprint.route("/recipes/<int:recipe_id>", methods=["GET"])
@token_required
def get_recipe_details(recipe_id):
    """Get details of a specific recipe."""
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
        
    recipe_data = {
        "recipe_name": recipe.recipe_name,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "created_at": recipe.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "user": recipe.user.username,
        "tags": [tag.name for tag in recipe.tags]
    }
    return jsonify(recipe_data), 200


@recipe_blueprint.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@token_required
def delete_recipe(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"}), 200
