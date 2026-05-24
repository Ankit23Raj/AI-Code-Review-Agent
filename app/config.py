from dotenv import load_dotenv
import os

from app.utils.logger import log

# Load environment variables from the local .env file.
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Confirm the token exists without printing the token itself.
log(f"GitHub token loaded: {bool(GITHUB_TOKEN)}")

