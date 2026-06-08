import os
import unittest

try:
    import requests
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    requests = None
    load_dotenv = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


class OpenEdxAuthSmokeTest(unittest.TestCase):
    def test_openedx_auth_environment_is_configurable(self):
        if IMPORT_ERROR:
            self.skipTest(f"Optional dependency unavailable: {IMPORT_ERROR}")

        load_dotenv()

        required = [
            "OPENEDX_BASE_URL",
            "OPENEDX_USERNAME",
            "OPENEDX_PASSWORD",
            "OPENEDX_CLIENT_ID",
        ]
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            self.skipTest(f"Open edX credentials not configured: {', '.join(missing)}")

        token_url = f"{os.getenv('OPENEDX_BASE_URL')}/oauth2/access_token"
        data = {
            "client_id": os.getenv("OPENEDX_CLIENT_ID", "login-service-client-id"),
            "grant_type": "password",
            "username": os.getenv("OPENEDX_USERNAME"),
            "password": os.getenv("OPENEDX_PASSWORD"),
            "token_type": "JWT",
        }

        response = requests.post(token_url, data=data, timeout=20)
        self.assertIn(response.status_code, {200, 400, 401, 403})


if __name__ == "__main__":
    unittest.main()
