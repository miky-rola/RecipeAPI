# Recipe API

The Recipe API is a RESTful web service built with Flask and SQLAlchemy, allowing users to manage recipes, tags, and user accounts. It provides endpoints for creating, updating, deleting, and retrieving recipes, as well as authentication and authorization features for user management.

## Features

**User Authentication**: Users can create accounts, log in, log out, and delete their accounts securely.

**Recipe Management**: Create, retrieve, update, and delete recipes. Each recipe includes details such as recipe name, ingredients, instructions, associated reviews and associated tags.

**Tagging System**: Recipes can be tagged with multiple categories for easy organization and filtering.

**Review System**: Users can leave reviews for recipes.

**RESTful API**: Follows RESTful principles for resource naming and HTTP methods.

**Secure Password Storage**: User passwords are securely hashed using bcrypt before storage.

## Installation

#### Clone the repository:

`git clone https://github.com/your_username/recipe-api.git`


#### Install dependencies:

`pip install -r requirements.txt`


### Set up environment variables:

Create a .env file in the project root directory.


### Define the following environment variables:

*`from dotenv import load_dotenv` and `import os` to be able to load it from the .env*

`HOSTNAME=os.getenv("your_database_hostname")`

`DATABASE=os.getenv("your_database_name")`

`USER=os.getenv("your_database_username")`

`PASSWORD=os.getenv("your_database_password")`

`PORT_ID=os.getenv("your_database_port")`

`SECURITY=os.getenv("your_flask_secret_key")`


### Run the Flask application:

`flask run`


## API Documentation

#### API Reference: Detailed documentation for all available endpoints and their usage.

### Usage

- Register a new user account using the /users endpoint.
    
  `POST http://127.0.0.1:5000/users HTTP/1.1
    content-type: application/json`
  `{
      "username": "eva",
      "password": "123"
  }`
  
  **Respone**
  
  `{
    "message": "User created successfully",
    "user_id": 3
  }`
  
- log in using  /login endpoint.
  
    `POST http://127.0.0.1:5000/login HTTP/1.1
  content-type: application/json`
  `{
      "username": "eva",
      "password": "123"
  }`
  
  **Response**
  
  `{
    "message": "Login successful"
  }`

- Log out using /logout
- 
  `DELETE http://127.0.0.1:5000/logout HTTP/1.1
  content-type: application/json`
  
  **Response**
  
  `{
  "message": "Logged out successfully"
  }`
  
- Log in to obtain an authentication token.

- Use the provided token for authentication in subsequent requests.

  Create, retrieve, update, or delete recipes using the appropriate endpoints.
  **creating recipe**
  
    `POST http://127.0.0.1:5000/recipes/create HTTP/1.1
    content-type: application/json`
  
  `{
      "recipe_name": "Waakye",
      "ingredients": "Rice and beans",
      "instructions": "Put on fire"
  }`
  
  **Response**
  
  `{
    "message": "Recipe created successfully",
    "recipe_id": 3
  }`

   **Retrieve Recipes**
    `GET http://127.0.0.1:5000/recipes HTTP/1.1
      content-type: application/json`

  **Response**
  ` {
      "created_at": "2024-05-03 07:11:34",
      "ingredients": "Rice and beans",
      "instructions": "Put on fire",
      "recipe_id": 3,
      "recipe_name": "Waakye",
      "reviews": [
        "I love it"
      ],
      "tags": [
        "best recipe tag"
      ],
      "user": "eva"
    }`
  

- Tag recipes with categories using the /tags endpoint.

 Create, retrieve, update, or delete tags using the appropriate endpoints.
 
 **create tags**
 
 `POST http://127.0.0.1:5000/recipes/3/tags HTTP/1.1
  content-type: application/json`

`{
    "tag_name": "best recipe tag"
}`

**Response**

`{
  "message": "Tag created successfully"
}`
 

- Leave reviews for recipes using the /reviews endpoint.

   Create, retrieve, update, or delete reviews using the appropriate endpoints.
  
   **creating a review**
  
   `POST http://127.0.0.1:5000/recipes/3/reviews HTTP/1.1
    content-type: application/json`
  
  `{
      "review_content": "I love it"
  }`
  
  **Response**
  
  `{
    "message": "Review added successfully"
  }`


## Contributing

Contributions are welcome! If you would like to contribute to the development of the Recipe API, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them with descriptive messages.

3. Push your changes to your fork.

4. Submit a pull request to the main repository's develop branch.
