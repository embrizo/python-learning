import logging
import os
import config

# Determine log file path in the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "bank.log")

# Parse log level from config
level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

# Setup logger
logger = logging.getLogger(config.APP_NAME)
logger.setLevel(level)

# Clear existing handlers to avoid duplicates (important for pytest/interactive)
if logger.hasHandlers():
    logger.handlers.clear()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File Handler
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
