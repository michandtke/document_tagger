# app.py
import logging
from fasthtml.common import *
from config import log_config
from routes import init_services

# Configure logging
logging.basicConfig(
    level=getattr(logging, log_config['level']),
    format=log_config['format']
)

# Initialize FastHTML app
app = FastHTML()

# Initialize services and register routes
init_services(app)

# Run the application
if __name__ == "__main__":
    serve()