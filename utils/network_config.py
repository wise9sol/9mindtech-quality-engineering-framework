# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""Network test constants. Import BASE_URL directly from utils.config."""

import os

from dotenv import load_dotenv

load_dotenv()

LOGIN_PATH = "/login"
VALID_USERNAME = os.getenv("TEST_USERNAME", "tomsmith")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "SuperSecretPassword!")
SUCCESS_PATH = "/secure"
