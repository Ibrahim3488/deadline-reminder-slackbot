import requests
from auth import get_access_token


def get_deadlines_from_openedx():
    token = get_access_token()

    if not token:
        print("No Open edX token available.")
        return []

    headers = {
        "Authorization": f"JWT {token}"
    }

    api_url = "https://sandbox.openedx.org/api/deadlines"

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()

    print("Failed to fetch deadlines:", response.status_code, response.text)
    return []
if __name__ == "__main__":
    deadlines = get_deadlines_from_openedx()
    print("Deadlines:", deadlines)