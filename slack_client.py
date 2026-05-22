import requests


def send_slack_message(webhook_url, message):
    try:
        response = requests.post(webhook_url, json=message)
        print(response.status_code, response.text)
        return True

    except Exception as error:
        print("Slack sending failed:", error)
        return False