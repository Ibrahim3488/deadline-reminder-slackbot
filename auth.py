import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENEDX_BASE_URL = os.getenv("OPENEDX_BASE_URL")
OPENEDX_USERNAME = os.getenv("OPENEDX_USERNAME")
OPENEDX_PASSWORD = os.getenv("OPENEDX_PASSWORD")
OPENEDX_CLIENT_ID = os.getenv("OPENEDX_CLIENT_ID", "login-service-client-id")


def get_access_token():
    token_url = f"{OPENEDX_BASE_URL}/oauth2/access_token"

    data = {
        "client_id": OPENEDX_CLIENT_ID,
        "grant_type": "password",
        "username": OPENEDX_USERNAME,
        "password": OPENEDX_PASSWORD,
        "token_type": "JWT",
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200 and response.text:
        token_data = response.json()
        return token_data.get("access_token")

    print("Authentication failed or empty response")
    print("Status:", response.status_code)
    print("Response:", repr(response.text))
    return None
if __name__ == "__main__":
    token = get_access_token()
    print("Token:", token)