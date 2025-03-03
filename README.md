# API Documentation

## Overview
This API provides endpoints for user authentication and text generation. It allows users to register, log in, and generate text responses using an AI service.


## Tools Used
- **PostgreSQL** (Database)
- **Python** (Flask Framework)
- **Docker** (Containerization)

## Setting Up the Project
### Using Docker
To set up and run the project with Docker, use the following command:
```sh
docker compose up -d --build
```
This will build and start the necessary containers for the application.

## Unit Testting

I have added a couple of test suites that covers edge cases
simply run

```sh
docker compose exec app pytest tests/
```


## Swagger Documentation
The API documentation is available at the base URL `/` on port `5000`. Access it in your browser to explore and test the endpoints.


### Base URL
The API is available at `http://localhost:5000/`. The Swagger documentation is accessible at the root endpoint `/`.

## Authentication
All protected endpoints require a JSON Web Token (JWT) for authentication.

### Register a New User
**Endpoint:** `POST /api/users`

**Request Body:**
```json
{
  "username": "example_user",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "example_user"
}
```

### User Login
**Endpoint:** `POST /api/login`

**Request Body:**
```json
{
  "username": "example_user",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "your_jwt_token_here"
}
```

Use the returned JWT token in the `Authorization` header for authenticated requests:
```
Authorization: Bearer your_jwt_token_here
```

## Generated Text Endpoints

### Get All Generated Texts
**Endpoint:** `GET /api/generated-text`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "prompt": "Hello AI",
    "response": "Hi there!",
    "timestamp": "2024-03-04T12:00:00Z"
  }
]
```

### Generate a New Text
**Endpoint:** `POST /api/generated-text`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Request Body:**
```json
{
  "prompt": "Tell me a joke"
}
```

**Response:**
```json
{
  "id": 2,
  "user_id": 1,
  "prompt": "Tell me a joke",
  "response": "Why did the chicken cross the road? To get to the other side!",
  "timestamp": "2024-03-04T12:05:00Z"
}
```

### Get a Specific Generated Text
**Endpoint:** `GET /api/generated-text/{id}`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "prompt": "Hello AI",
  "response": "Hi there!",
  "timestamp": "2024-03-04T12:00:00Z"
}
```

### Update a Generated Text
**Endpoint:** `PUT /api/generated-text/{id}`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Request Body:**
```json
{
  "prompt": "Tell me a fun fact"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "prompt": "Tell me a fun fact",
  "response": "Did you know that honey never spoils?",
  "timestamp": "2024-03-04T12:10:00Z"
}
```

### Delete a Generated Text
**Endpoint:** `DELETE /api/generated-text/{id}`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
{
  "message": "Deleted successfully"
}
```


c. Akinyemi Sodiq