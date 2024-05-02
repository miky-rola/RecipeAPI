Recipe API:
The Recipe API is a RESTful web service built with Flask and SQLAlchemy, allowing users to manage recipes, tags, and user accounts. It provides endpoints for creating, updating, deleting, and retrieving recipes, as well as authentication and authorization features for user management.

Features:::
User Authentication: Users can create accounts, log in, log out, and delete their accounts securely.
Recipe Management: Create, retrieve, update, and delete recipes. Each recipe includes details such as recipe name, ingredients, instructions, associated reviews and associated tags.
Tagging System: Recipes can be tagged with multiple categories for easy organization and filtering.
Review System: Users can leave reviews for recipes.
RESTful API: Follows RESTful principles for resource naming and HTTP methods.
Secure Password Storage: User passwords are securely hashed using bcrypt before storage.
