"""
Models package initialization.
This module imports all models to ensure they are registered with SQLAlchemy.
"""

from app.models.user import User

# Export all models
__all__ = ["User"]
