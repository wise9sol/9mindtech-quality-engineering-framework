import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv("BASE_URL", "https://example.com")
ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")