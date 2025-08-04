import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    # Initialize and run the application
    try:
        app = create_app()

        # Get configuration from environment
        host = os.getenv("FLASK_HOST", "0.0.0.0")
        port = int(os.getenv("FLASK_PORT", 5000))
        debug = os.getenv("FLASK_ENV", "production") == "development"

        logger.info(f"Starting Flask application on {host}:{port}")
        logger.info(f"Debug mode: {debug}")

        # Run the application
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise


if __name__ == "__main__":
    main()
