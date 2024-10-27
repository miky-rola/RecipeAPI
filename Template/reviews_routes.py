from flask import Blueprint, jsonify, request, session
from models import Review, Recipe, Users, db
from user_routes import token_required

review_blueprint = Blueprint("review_blueprint", __name__)


@review_blueprint.route("/recipes/<int:recipe_id>/reviews", methods=["POST"])
@token_required
def leave_review(recipe_id):
    """Leave a review for a recipe."""
    try:
        data = request.get_json()
        review_content = data.get("review_content")
        is_anonymous = data.get("anonymous", False)

        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"message": "Recipe not found"}), 404

        current_user_id = session.get("user_id")

        new_review = Review(
            review_content=review_content,
            user_id=current_user_id if not is_anonymous else None,
            recipe_id=recipe_id,
            is_anonymous=is_anonymous
        )

        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "An error occurred while adding the review"}), 500 
    

@review_blueprint.route("/recipes/<string:recipe_name>/reviews", methods=["GET"])
@token_required
def get_recipe_reviews(recipe_name):
    """Get all reviews for a specific recipe."""
    recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    reviews = Review.query.filter_by(recipe_id=recipe.id).all()
    review_data = []
    for review in reviews:
        if review.is_anonymous:
            reviewer = "Anonymous"
        else:
            reviewer = Users.query.get(review.user_id).username
        review_info = {
            "review_id": review.id,
            "review_content": review.review_content,
            "is_anonymous": review.is_anonymous,
            "reviewer": reviewer
        }
        review_data.append(review_info)
    return jsonify({"reviews": review_data}), 200

@review_blueprint.route("/reviews/<int:review_id>", methods=["DELETE"])
@token_required
def delete_review(review_id):
    """Delete a review."""
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404
    
    if review.user_id != session.get("user_id"):
        return jsonify({"message": "You are not authorized to delete this review"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted successfully"}), 200