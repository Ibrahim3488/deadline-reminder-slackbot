import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENEDX_BASE_URL = os.getenv("OPENEDX_BASE_URL")
OPENEDX_USERNAME = os.getenv("OPENEDX_USERNAME")
OPENEDX_PASSWORD = os.getenv("OPENEDX_PASSWORD")
OPENEDX_CLIENT_ID = os.getenv("OPENEDX_CLIENT_ID", "login-service-client-id")

token_url = f"{OPENEDX_BASE_URL}/oauth2/access_token"

data = {
    "client_id": OPENEDX_CLIENT_ID,
    "grant_type": "password",
    "username": OPENEDX_USERNAME,
    "password": OPENEDX_PASSWORD,
    "token_type": "JWT",
}

response = requests.post(token_url, data=data)
print(response.headers)

print("Status:", response.status_code)
print("Headers:", response.headers)
print("Response text:", repr(response.text))
print("Content length:", len(response.content))