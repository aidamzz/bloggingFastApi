# bloggingFastApi
FastAPI Blogging Platform
This is a simple blogging platform built using FastAPI and SQLAlchemy. It provides APIs for managing blog posts and comments, as well as user authentication using JWT tokens.

# FastAPI Application Features Summary

This FastAPI application provides a robust set of features centered around blog management, user authentication, and comments handling. Below is a summary of the core functionalities exposed through the API endpoints.

## Features

### User Management

- **User Registration:** Allows new users to register with a username, email, and password.
- **User Authentication:** Supports user login, returning JWT tokens for authenticated sessions.

### Blog Posts

- **Create Posts:** Authenticated users can create new blog posts.
- **Read Posts:** Supports fetching all posts with optional filtering by username, date, and tags. Individual posts can be fetched by their ID.
- **Update Posts:** Owners of posts can update their content.
- **Delete Posts:** Owners can delete their posts.

### Comments

- **Add Comments:** Users can comment on posts after successful authentication.
- **View Comments:** Fetches all comments for a specific post.
- **Delete Comments:** Comment creators can delete their comments.

## Authentication and Security

- Utilizes JWT for securing endpoints that require user authentication.
- Employs bcrypt hashing for secure password storage.
- Enforces access controls ensuring users can only modify or delete their own posts and comments.

## Implementation Highlights

- **Modular Design:** Features are encapsulated in separate modules (`users.py`, `posts.py`, and `comments.py`) for clarity and maintainability.
- **ORM Integration:** Leverages SQLAlchemy for database operations, enhancing code readability and database management.
- **Security Practices:** Adheres to security best practices, including password hashing and token-based authentication.

## Getting Started

To interact with the API, start by registering as a new user to obtain JWT tokens required for authenticated endpoints. Explore the `/docs` or `/redoc` routes for interactive API documentation and testing capabilities provided by FastAPI

# FastAPI Blogging Platform Setup Guide

Enhance your development experience with the FastAPI blogging platform, offering a suite of features for blog management. This guide will walk you through setting up and running the platform locally.

## Prerequisites

Ensure you have the following installed:

- Python 3.6+
- pip
- MySQL Server

## Installation Steps

### 1. Clone the Repository

Clone and navigate into the project directory:

```shell
git clone https://github.com/aidamzz/fastapi-blogging-platform.git
cd fastapi-blogging-platform
```
## Database Setup

To properly set up and configure your database for use with the FastAPI blogging platform, follow these steps:

### Create a MySQL Database

First, you need to create a new MySQL database that the application will use to store its data. Log into your MySQL server and run the following command:

```sql
CREATE DATABASE blogging;
```
## Running the Application

With the database configured and dependencies installed, you're now ready to run the FastAPI application. This section outlines the steps to start your server and access the application.

### Start the FastAPI Server

Use Uvicorn, an ASGI server, to run your FastAPI application. Execute the following command in the terminal from the root of your project directory:

```bash
uvicorn main:app --reload
```
The `--reload` flag is particularly useful during development as it automatically reloads the server when code changes are detected, helping you to see updates in real-time without manually restarting the server.

## Accessing the Application

Once the server is running, your FastAPI application is accessible at:

http://localhost:8000

You can open this URL in your web browser to interact with your application. FastAPI also provides interactive API documentation that can be accessed at:

http://localhost:8000/docs

This documentation is generated automatically and offers a user-friendly interface to test the API endpoints directly from the browser.

## Testing with Postman

The project includes a Postman collection (`Blogging.postman_collection.json`) which contains predefined requests for testing the API endpoints. To use this collection:

1. Open Postman and click on the `Import` button.
2. Choose `File` and upload the `Blogging.postman_collection.json` file from your project directory.
3. After importing, you'll see the collection in your Postman sidebar, ready for use.

By following these steps, you'll have your FastAPI blogging platform running locally and be ready to start testing and further development.


# Users API Endpoints

This documentation outlines the Users API of our FastAPI application, focusing on user management including registration, and authentication via JWT tokens.

## Getting Started

The Users API allows for user registration and login, providing JWT tokens for authenticated access to protected endpoints.

## API Endpoints

### Register a User

Allows for the registration of a new user.

- **Endpoint:** `POST /users/`
- **Authorization:** Not required
- **Request Body:**
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "password123"
    }
    ```
- **Response:** The newly created User object, excluding the password.
    ```json
    {
      "id": "Generated User ID",
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```
- **Status Codes:**
    - `200 OK` on success
    - `400 Bad Request` if the username is already registered

### Obtain an Access Token

Authenticates a user and returns a JWT token for accessing protected endpoints.

- **Endpoint:** `POST /token`
- **Authorization:** Not required
- **Request Body:**
    - Use `application/x-www-form-urlencoded` content type
    - Fields: `username` and `password`
    ```plaintext
    username=newuser&password=password123
    ```
- **Response:** A JWT access token.
    ```json
    {
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
- **Status Codes:**
    - `200 OK` on successful authentication
    - `400 Bad Request` for incorrect username or password

## Error Responses

Common error responses include:

- `400 Bad Request`: Indicates issues with the request, such as already existing username during registration or incorrect login credentials.
- `422 Unprocessable Entity`: Returned when request validation fails, often due to improperly formatted request bodies.

## Authorization

Protected endpoints require an `Authorization` header with a Bearer token obtained from the login endpoint:


Authorization: Bearer <your_jwt_token_here>
# Authentication Mechanism

This section explains the authentication system implemented in the FastAPI application, focusing on user authentication, password hashing, and JWT token management as defined in `auth.py`.

## Overview

The application uses JWT (JSON Web Tokens) for authenticating users and securing access to certain API endpoints. Passwords are securely hashed using the `bcrypt` algorithm, ensuring that plain-text passwords are never stored or transmitted.

## Key Components

### Password Hashing

- **Mechanism:** Utilizes `passlib` and its `bcrypt` context for hashing and verifying passwords.
- **Usage:** Upon user registration, passwords are hashed before being stored in the database. For login, the submitted password is verified against the stored hash.

### JWT Token Generation and Verification

- **Library Used:** `python-jose` for handling JWT operations.
- **Key Features:**
    - **Token Creation:** Upon successful login, a JWT token is generated, containing the `sub` claim with the username and an expiry time defined by `ACCESS_TOKEN_EXPIRE_MINUTES`.
    - **Token Verification:** Each request to a protected endpoint must include this token in the Authorization header. The token is validated for integrity and expiry.

### Security Settings

- **Secret Key and Algorithm:**
    - `SECRET_KEY`: Used to sign JWT tokens. It's crucial to keep this key secret and secure.
    - `ALGORITHM`: Specifies the algorithm used for JWT encoding and decoding, set to `HS256` by default.
    - `ACCESS_TOKEN_EXPIRE_MINUTES`: Defines the lifespan of each access token.

## Dependencies

Ensure the following dependencies are installed in your environment for the authentication system to function correctly:

- `passlib`
- `python-jose`
- `fastapi`
- `sqlalchemy` for database interactions

## Implementation Highlights

# Example of password hashing
hashed_password = get_password_hash("your_password")

# Example of token generation
access_token = create_access_token(data={"sub": "username"})

# Example of password verification
is_valid = verify_password("plain_password", "hashed_password")

# Posts API Endpoints

This document outlines the Posts API of our FastAPI application, enabling users to manage blog posts including creating new posts, reading existing ones, updating, and deleting them. Operations on posts require user authentication.

## Getting Started

Interaction with the Posts API requires a valid JWT token for authentication. Make sure to include this token in the Authorization header as a Bearer token for endpoints that require authentication.

## API Endpoints

### Create a Post

Creates a new blog post.

- **Endpoint:** `POST /`
- **Authorization:** Required
- **Request Body:**
    ```json
    {
      "title": "Post Title",
      "content": "Post content",
      "author_id": "Author's User ID",  
      "tags": "Optional tags separated by commas"
    }
    ```
- **Response:** The created Post object.
    ```json
    {
      "id": "Generated Post ID",
      "title": "Post Title",
      "content": "Post content",
      "created_at": "Creation timestamp",
      "author_id": "Author's User ID",
      "tags": "Optional tags"
    }
    ```

### Read Posts

Retrieves a list of posts, with optional filters.

- **Endpoint:** `GET /`
- **Authorization:** Not required
- **Optional Query Parameters:** `username`, `date`, `tags`
- **Response:** An array of Post objects.
    ```json
    [
      {
        "id": "Post ID",
        "title": "Post Title",
        "content": "Post content",
        "created_at": "Creation timestamp",
        "author_id": "Author's User ID",
        "tags": "Optional tags"
      },
      
    ]
    ```

### Read a Single Post

Retrieves a specific post by ID.

- **Endpoint:** `GET /{post_id}`
- **Authorization:** Not required
- **Response:** A single Post object.
    ```json
    {
      "id": "Post ID",
      "title": "Post Title",
      "content": "Post content",
      "created_at": "Creation timestamp",
      "author_id": "Author's User ID",
      "tags": "Optional tags"
    }
    ```

### Update a Post

Updates an existing post.

- **Endpoint:** `PUT /{post_id}`
- **Authorization:** Required (users can only update their own posts)
- **Request Body:**
    ```json
    {
      "title": "Optional new title",
      "content": "Optional new content",
      "tags": "Optional new tags"
    }
    ```
- **Response:** The updated Post object.

### Delete a Post

Deletes a specific post by ID.

- **Endpoint:** `DELETE /{post_id}`
- **Authorization:** Required (users can only delete their own posts)
- **Response:** A confirmation message.
    ```json
    {
      "message": "Post successfully deleted"
    }
    ```

## Error Responses

You might encounter the following errors:

- `404 Not Found`: The specified post does not exist.
- `401 Unauthorized`: The request lacks valid authentication credentials.
- `422 Unprocessable Entity`: Validation of the request body failed.

## Authorization

To access endpoints that require authentication, include an `Authorization` header with your Bearer token:

```Authorization: Bearer YOUR_JWT_TOKEN_HERE```

## Notes

- Date filtering format should comply with ISO 8601 standards.
- Ensure your requests adhere to the specified formats for successful API interaction.

# Comments API Endpoints

This document provides an overview and documentation for the Comments API endpoints of our FastAPI application. The Comments API allows for the creation, retrieval, and deletion of comments on blog posts by authenticated users.

## Getting Started

To interact with the Comments API, users must be authenticated and authorized. Authentication is handled through JWT tokens provided upon login. Ensure you have obtained a valid token and include it in the Authorization header as a Bearer token for endpoints that require authentication.

## API Endpoints

### Create a Comment

Creates a new comment on a specified post.

- **Endpoint:** `POST /posts/{post_id}/comments/`
- **Authorization:** Required
- **Request Body:**
    ```json
    {
      "text": "Your comment here",
      "author_id": "Your author ID here"
    }
    ```
- **Response:** A JSON representation of the created comment.
    ```json
    {
      "id": "Generated comment ID",
      "text": "Your comment here",
      "author_id": "Your author ID here",
      "post_id": "The post ID this comment is associated with",
      "created_at": "Timestamp"
    }
    ```

### Get Comments for a Post

Retrieves all comments associated with a specific post.

- **Endpoint:** `GET /posts/{post_id}/comments/`
- **Authorization:** Not required
- **Response:** An array of comments for the specified post.
    ```json
    [
      {
        "id": "Comment ID",
        "text": "Comment text",
        "author_id": "Author ID",
        "post_id": "Associated post ID",
        "created_at": "Timestamp"
      },
      ...
    ]
    ```

### Delete a Comment

Deletes a specific comment by ID. Users can only delete their own comments.

- **Endpoint:** `DELETE /comments/{comment_id}`
- **Authorization:** Required
- **Response:** A confirmation message indicating successful deletion.
    ```json
    {
      "message": "Comment successfully deleted"
    }
    ```

## Error Responses

Common error responses include:

- `404 Not Found`: Returned when a specified post or comment does not exist.
- `401 Unauthorized`: Returned when the request lacks a valid authentication token or does not have permission to perform the requested operation.
- `422 Unprocessable Entity`: Returned when request validation fails.

## Authorization

Endpoints requiring authorization expect an `Authorization` header with a Bearer token obtained after successful login.

```Bearer YOUR_JWT_TOKEN_HERE```


