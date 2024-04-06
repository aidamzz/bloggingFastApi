# bloggingFastApi
FastAPI Blogging Platform
This is a simple blogging platform built using FastAPI and SQLAlchemy. It provides APIs for managing blog posts and comments, as well as user authentication using JWT tokens.

Features
User registration and login with JWT authentication
CRUD operations for blog posts
CRUD operations for comments on blog posts
Filtering blog posts by date, author, or tags
Setup
Installation
Clone the repository:

git clone https://github.com/yourusername/fastapi-blogging-platform.git
Install dependencies:

pip install -r requirements.txt
Database Setup
Create a MySQL database for the blogging platform.
Update the SQLALCHEMY_DATABASE_URL variable in main.py with your MySQL username, password, and database name.
Running the Application
Start the FastAPI server using Uvicorn:

uvicorn main:app --reload
The server should now be running on http://localhost:8000.

User Registration
To register a new user, send a POST request to /register/ with the following JSON payload:

json
Copy code
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password"
}
User Login
To log in as a registered user, send a POST request to /login/ with the following JSON payload:

json
Copy code
{
    "username": "existinguser",
    "password": "password"
}
The response will include an access token which you can use for authentication in subsequent requests.

Blog Posts
Create a Post: Send a POST request to /posts/ with the necessary parameters: title, content, author, and optionally tags.
Retrieve All Posts: Send a GET request to /posts/ to retrieve all blog posts. You can also filter posts by filter_date, author, or tags.
Retrieve a Post by ID: Send a GET request to /posts/{post_id} to retrieve a specific post by its ID.
Update a Post: Send a PUT request to /posts/{post_id} with updated post details.
Delete a Post: Send a DELETE request to /posts/{post_id} to delete a post by its ID.
Comments
Create a Comment: Send a POST request to /posts/{post_id}/comments/ with the author and text parameters to add a comment to a post.
Retrieve Comments: Send a GET request to /posts/{post_id}/comments/ to retrieve all comments for a post.
Delete a Comment: Send a DELETE request to /comments/{comment_id} to delete a comment by its ID.