import logging
from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from app import db
from app.models.user import User
from flasgger import swag_from

# Create blueprint
api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


@api_bp.route("/users", methods=["GET"])
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "department",
                "in": "query",
                "type": "string",
                "required": False,
                "description": "Filter users by department",
            }
        ],
        "responses": {
            200: {
                "description": "A list of users",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {"type": "array", "items": {"type": "object"}},
                        "count": {"type": "integer"},
                        "filters": {"type": "object"},
                    },
                },
            }
        },
    }
)
def get_users():
    """
    Get all users or filter by department.
    """
    try:
        # Get query parameters
        department = request.args.get("department")

        # Build query
        query = User.query

        if department:
            query = query.filter(User.department.ilike(f"%{department}%"))

        # Execute query
        users = query.order_by(User.created_at.desc()).all()

        # Convert to dictionaries
        users_data = [user.to_dict() for user in users]

        logger.info(f"Retrieved {len(users_data)} users")

        return (
            jsonify(
                {
                    "success": True,
                    "data": users_data,
                    "count": len(users_data),
                    "filters": {"department": department},
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Failed to retrieve users",
                    "message": str(e),
                }
            ),
            500,
        )


@api_bp.route("/users/<int:user_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "User ID",
            }
        ],
        "responses": {
            200: {
                "description": "User found",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {"type": "object"},
                    },
                },
            },
            404: {
                "description": "User not found",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "error": {"type": "string"},
                        "message": {"type": "string"},
                    },
                },
            },
        },
    }
)
def get_user(user_id):
    """
    Get a specific user by ID.
    """
    try:
        user = User.query.get(user_id)

        if not user:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "User not found",
                        "message": f"No user found with ID {user_id}",
                    }
                ),
                404,
            )

        logger.info(f"Retrieved user {user_id}")

        return (
            jsonify({"success": True, "data": user.to_dict(include_sensitive=True)}),
            200,
        )

    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Failed to retrieve user",
                    "message": str(e),
                }
            ),
            500,
        )


@api_bp.route("/users", methods=["POST"])
@swag_from(
    {
        "tags": ["Users"],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["name", "email", "department"],
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "department": {"type": "string"},
                        },
                    }
                }
            },
        },
        "responses": {
            201: {
                "description": "User created successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {"type": "object"},
                        "message": {"type": "string"},
                    },
                },
            },
            400: {
                "description": "Invalid input",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "error": {"type": "string"},
                        "message": {"type": "string"},
                    },
                },
            },
            409: {
                "description": "Email already exists",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "error": {"type": "string"},
                        "message": {"type": "string"},
                    },
                },
            },
        },
    }
)
def create_user():
    """
    Create a new user.
    """
    try:
        # Get request data
        data = request.get_json()

        if not data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "No data provided",
                        "message": "Request body must contain JSON data",
                    }
                ),
                400,
            )

        # Validate required fields
        required_fields = ["name", "email", "department"]
        missing_fields = [
            field for field in required_fields if field not in data or not data[field]
        ]

        if missing_fields:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Missing required fields",
                        "message": f'Required fields: {", ".join(missing_fields)}',
                    }
                ),
                400,
            )

        # Check if email already exists
        existing_user = User.find_by_email(data["email"])
        if existing_user:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Email already exists",
                        "message": f'A user with email {data["email"]} already exists',
                    }
                ),
                409,
            )

        # Create new user
        user = User(
            name=data["name"], email=data["email"], department=data["department"]
        )

        # Save to database
        user.save()

        logger.info(f"Created new user {user.id}: {user.name}")

        return (
            jsonify(
                {
                    "success": True,
                    "data": user.to_dict(),
                    "message": "User created successfully",
                }
            ),
            201,
        )

    except exc.IntegrityError as e:
        db.session.rollback()
        logger.error(f"Database integrity error creating user: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Database constraint violation",
                    "message": "User with this email may already exist",
                }
            ),
            409,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return (
            jsonify(
                {"success": False, "error": "Failed to create user", "message": str(e)}
            ),
            500,
        )
