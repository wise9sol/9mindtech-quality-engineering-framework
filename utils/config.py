import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT")