"""
Database helper utilities for the microservice application.
Contains functions for initializing sample data and database operations.
"""

import logging
from datetime import datetime, date
from app import db
from app.models.user import User

logger = logging.getLogger(__name__)


def initialize_sample_data():
    """
    Initialize the database with sample user data if no users exists.
    This creates 8 sample employee records for demo puproses
    """
    try:
        # Check if users already exist
        existing_users_count = User.query.count()

        if existing_users_count > 0:
            logger.info(
                f"Database already contains {existing_users_count} users, skipping sample data initialization"
            )
            return

        logger.info("Initializing database with sample data..")

        sample_users = [
            {
                "name": "Alice Johnson",
                "email": "alice.johnson@company.com",
                "department": "Engineering",
            },
            {
                "name": "Bob Smith",
                "email": "bob.smith@company.com",
                "department": "Marketing",
            },
            {
                "name": "Carol Williams",
                "email": "carol.williams@company.com",
                "department": "Engineering",
            },
            {
                "name": "David Brown",
                "email": "david.brown@company.com",
                "department": "Sales",
            },
            {
                "name": "Emma Davis",
                "email": "emma.davis@company.com",
                "department": "HR",
            },
            {
                "name": "Frank Miller",
                "email": "frank.miller@company.com",
                "department": "Engineering",
            },
            {
                "name": "Grace Wilson",
                "email": "grace.wilson@company.com",
                "department": "Finance",
            },
            {
                "name": "Henry Taylor",
                "email": "henry.taylor@company.com",
                "department": "Operations",
            },
        ]

        created_count = 0
        for user_data in sample_users:
            try:
                user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    department=user_data["department"],
                )
                db.session.add(user)
                created_count += 1
            except Exception as e:
                logger.error(f"Error creating user {user_data['name']}: {str(e)}")
                continue

        db.session.commit()

        logger.info(f"Successfully created {created_count} sample users")

    except Exception as e:
        logger.error(f"Failed to initialize sample data: {str(e)}")
        db.session.rollback()
        raise
