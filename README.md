# Heddy Backend 
Heddy Backend 

# API 명세서 

## Base URL
```
/api/v1
```

## Authentication
Bearer token authentication is used for protected endpoints.
```
Authorization: Bearer <access_token>
```

## Endpoints

### Health Check
#### GET `/health`
Check if the API is running.

**Response**
```json
{
    "status": "healthy"
}
```

### Version Check
#### GET `/version`
Get current API version information.

**Response**
```json
{
    "version": "1.0.0",
    "api_version": "v1"
}
```

### User Management
#### POST `/user`
Create a new user account.

**Request Body**
```json
{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "secretpassword"
}
```

**Validation Rules**
- `email`: Must be a valid email address
- `username`: 3-50 characters
- `password`: Minimum 8 characters

**Response**
- `200`: Successfully created user
- `400`: Email already registered

#### GET `/user/{user_id}`
Get user information by user ID.

**Path Parameters**
- `user_id`: User's unique identifier

**Response**
- `200`: User information
- `404`: User not found

### Protected Endpoints
The following endpoints require authentication:

#### PUT `/profiles/me`
Update current user's profile.

**Request Body**
```json
{
    "email": "new@example.com",
    "username": "newusername",
    "full_name": "New Name"
}
```

**Response**
- `200`: Updated profile information
- `401`: Unauthorized
- `403`: Forbidden

#### GET `/profiles/{username}`
Get user profile by username.

**Path Parameters**
- `username`: User's username

**Response**
- `200`: Profile information
- `404`: Profile not found

## Error Responses
Standard error responses follow this format:
```json
{
    "detail": "Error message"
}
```

Common HTTP Status Codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error

## Data Models

### User Model
```json
{
    "id": "string",
    "email": "string",
    "username": "string",
    "full_name": "string",
    "is_active": boolean,
    "is_superuser": boolean,
    "created_at": "datetime",
    "updated_at": "datetime",
    "last_login": "datetime"
}
```

### Profile Model
```json
{
    "username": "string",
    "email": "string",
    "full_name": "string"
}
```

## Rate Limiting
- Maximum 100 requests per minute per IP address
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## CORS
Allowed origins:
- http://localhost:3000
- http://localhost:8000
- http://localhost:5173

## File Upload Constraints
- Maximum file size: 5MB
- Allowed file types:
  - image/jpeg
  - image/png
  - application/pdf


# Package Error
```
    Traceback (most recent call last):
    File "C:\Users\kzsc5\.conda\envs\heddy\Lib\site-packages\passlib\handlers\bcrypt.py", line 620, in loadbackend_mixin
        version = bcrypt._about.version
                ^^^^^^^^^^^^^^^^^
    AttributeError: module 'bcrypt' has no attribute 'about__'
```
- 문제 : 두개의 bcrypt 와 passlib의 버전 충돌

- 해결 : pip install bcrypt==4.0.1 passlib==1.7.4
