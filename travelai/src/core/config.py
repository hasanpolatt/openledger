import os
from pathlib import Path

from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Database configuration
POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
POSTGRES_DB: str = os.getenv("POSTGRES_DB")

# Database URL
SQLALCHEMY_DATABASE_URI: str = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
