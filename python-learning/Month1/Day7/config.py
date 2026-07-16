import os

# Get path of .env relative to this file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
except ImportError:
    # Fallback to manual parsing if python-dotenv is not installed
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

APP_NAME = os.getenv("APP_NAME", "BankCLI")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_FILE = os.getenv("DATA_FILE", "account.json")

# Ensure DATA_FILE is resolved relative to the script directory if it's relative
if not os.path.isabs(DATA_FILE):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(script_dir, DATA_FILE)
