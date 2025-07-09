import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logger
logger = logging.getLogger("bakery_planner")
logger.setLevel(logging.DEBUG)  # Change to INFO or WARNING in production

# Create file handler for log output
file_handler = logging.FileHandler("logs/bakery_planner.log")
file_handler.setLevel(logging.DEBUG)

# Create console handler for real-time debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
