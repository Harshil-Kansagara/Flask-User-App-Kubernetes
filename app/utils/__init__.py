"""
Utilities package initialization.
This module exports utility functions for the application.
"""

from app.utils.db_helpers import initialize_sample_data

# Export utility functions
__all__ = ["initialize_sample_data"]
