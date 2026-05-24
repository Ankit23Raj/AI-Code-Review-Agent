from dotenv import find_dotenv, load_dotenv
import os

from app.utils.logger import log

dotenv_path = find_dotenv()
ENV_LOADED = load_dotenv(dotenv_path)

# This helps verify that the environment file was loaded at startup.
log(
	f".env loaded: {ENV_LOADED}"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

