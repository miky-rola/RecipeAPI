from flask import Blueprint, jsonify, request, session
from models import Review, Recipe, Users, db
from user_routes import token_required

# Creating a Blueprint for review-related routes
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

        # Create a new review object and associate it with the recipe
        new_review = Review(
            review_content=review_content,
            user_id=current_user_id if not is_anonymous else None,
            recipe_id=recipe_id,
            is_anonymous=is_anonymous
        )

        # Add new review to database
        db.session.add(new_review)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        print("Error:", str(e))
        # Return error message if an exception occurs
        return jsonify({"message": "An error occurred while adding the review"}), 500 
    

@review_blueprint.route("/recipes/<string:recipe_name>/reviews", methods=["GET"])
@token_required
def get_recipe_reviews(recipe_name):
    """Get all reviews for a specific recipe."""
    recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    # Query all reviews for the recipe
    reviews = Review.query.filter_by(recipe_id=recipe.id).all()
    review_data = []
    for review in reviews:
        if review.is_anonymous:
            reviewer = "Anonymous"
        else:
            reviewer = Users.query.get(review.user_id).username
        # Construct response data for each review
        review_info = {
            "review_id": review.id,
            "review_content": review.review_content,
            "is_anonymous": review.is_anonymous,
            "reviewer": reviewer
        }
        review_data.append(review_info)
    # Return list of reviews
    return jsonify({"reviews": review_data}), 200

@review_blueprint.route("/reviews/<int:review_id>", methods=["DELETE"])
@token_required
def delete_review(review_id):
    """Delete a review."""
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404
    
    # Check if the user is authorized to delete the review
    if review.user_id != session.get("user_id"):
        return jsonify({"message": "You are not authorized to delete this review"}), 403

    # Delete review from database
    db.session.delete(review)
    db.session.commit()
    # Return success message
    return jsonify({"message": "Review deleted successfully"}), 200