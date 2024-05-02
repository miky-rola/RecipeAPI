Recipe API

The Recipe API is a RESTful web service built with Flask and SQLAlchemy, allowing users to manage recipes, tags, and user accounts. It provides endpoints for creating, updating, deleting, and retrieving recipes, as well as authentication and authorization features for user management.

Features

User Authentication: Users can create accounts, log in, log out, and delete their accounts securely.

Recipe Management: Create, retrieve, update, and delete recipes. Each recipe includes details such as recipe name, ingredients, instructions, associated reviews and associated tags.

Tagging System: Recipes can be tagged with multiple categories for easy organization and filtering.

Review System: Users can leave reviews for recipes.

RESTful API: Follows RESTful principles for resource naming and HTTP methods.

Secure Password Storage: User passwords are securely hashed using bcrypt before storage.

Installation

Clone the repository:

git clone https://github.com/your_username/recipe-api.git


Install dependencies:

pip install -r requirements.txt


Set up environment variables:

Create a .env file in the project root directory.


Define the following environment variables:

import load_dotenv from dotenv and import os to be able to load it from the .env

HOSTNAME=your_database_hostname

DATABASE=os.getenv("your_database_name")

USER=os.getenv("your_database_username")

PASSWORD=os.getenv("your_database_password")

PORT_ID=os.getenv("your_database_port")

SECURITY=os.getenv("your_flask_secret_key")


Run the Flask application:

flask run


API Documentation

API Reference: Detailed documentation for all available endpoints and their usage.

Usage

Register a new user account using the /users endpoint.

log in using  /login endpoint.

Log out using /logout

Log in to obtain an authentication token.

Use the provided token for authentication in subsequent requests.

Create, retrieve, update, or delete recipes using the appropriate endpoints.

Tag recipes with categories using the /tags endpoint.

Create, retrieve, update, or delete tags using the appropriate endpoints.

Leave reviews for recipes using the /reviews endpoint.

Create, retrieve, update, or delete reviews using the appropriate endpoints.


Contributing

Contributions are welcome! If you would like to contribute to the development of the Recipe API, please follow these steps:

Fork the repository.

Create a new branch for your feature or bug fix.

Make your changes and commit them with descriptive messages.

Push your changes to your fork.

Submit a pull request to the main repository's develop branch.
