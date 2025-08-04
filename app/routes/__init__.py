"""
Routes package initialization.
This module exports all route blueprints.
"""

from app.routes.api import api_bp

# Export all blueprints
__all__ = ["api_bp"]
