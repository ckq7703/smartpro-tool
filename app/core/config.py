import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory (absolute path to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Storage Directories
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
TEMPLATES_WORD_DIR = os.path.join(BASE_DIR, "templates_word")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_UI_DIR = os.path.join(BASE_DIR, "templates")

# MySQL Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "smartpro_tools")

# Final Database URL (Pure MySQL)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Authentication & Secrets
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

# Default Admin (Internal use only)
ADMIN_USER = os.getenv("ADMIN_USER", "smartproadmin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "smartproadmin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "smartproadmin@gmail.com")

# Ensure directories exist
for folder in [EXPORTS_DIR, UPLOADS_DIR, TEMPLATES_WORD_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)
