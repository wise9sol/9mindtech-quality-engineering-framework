# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")
