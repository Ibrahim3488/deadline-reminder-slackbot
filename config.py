import os
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
OPENEDX_BASE_URL = os.getenv("OPENEDX_BASE_URL")
USE_OPENEDX = os.getenv("USE_OPENEDX", "False") == "True"

REMINDER_DAYS = int(os.getenv("REMINDER_DAYS", 3))

CHECK_TIME = os.getenv("CHECK_TIME", "09:00")