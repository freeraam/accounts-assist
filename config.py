import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Base path for data
BASE_DATA_DIR = "data"

# Google Sheets Credentials (path to JSON file)
# In a real app, this would be a secret.
GOOGLE_SHEETS_CREDENTIALS = "credentials.json"

# Supported file formats
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".pdf"]

# Categories
CATEGORIES = ["Purchase", "Sales", "CreditNote"]
