import json
import requests
import sys
from scheduler import start_scheduler
from logger import write_log
from slack_client import send_slack_message
from data_loader import load_json_file
from utils import get_priority_emoji, format_deadline_message
from config import (
    webhook_url,
    REMINDER_DAYS,
    CHECK_TIME
)
from pathlib import Path
from dotenv import dotenv_values
print("THIS IS THE MAIN FILE RUNNING")
print("MAIN FILE PATH:", __file__)
env_path = Path(__file__).parent / ".env"
config = dotenv_values(env_path)
webhook_url = config["SLACK_WEBHOOK_URL"]
base_url = config["OPENEDX_BASE_URL"]
client_id = config["OPENEDX_CLIENT_ID"]
client_secret = config["OPENEDX_CLIENT_SECRET"]
print("Slack loaded")
print("Open edX loaded")
def get_openedx_token():
    token_url = f"{base_url}/oauth2/access_token/"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(
        token_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
    )
    print("Final URL:", response.url)
    print("Status:", response.status_code)
    print("Headers:", response.headers)
    print("Response:", repr(response.text))
    if response.text.strip():
        return response.json()
    else:
        print("The server returned 200 but no JSON body.")
        return None
token_data = get_openedx_token()
print("Token data:", token_data)
if token_data:
    access_token = token_data.get("access_token")
    print("Access Token:", access_token)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    api_url = f"{base_url}/api/courses/v1/courses/"
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    print(response.text)
else:
    print("Token request failed")
def check_deadlines():
    USE_OPENEDX = True
    print("CHECK_DEADLINES STARTED")
    print("USE_OPENEDX =", USE_OPENEDX)
    if USE_OPENEDX:
        from openedx_api import get_deadlines_from_openedx
        deadlines = get_deadlines_from_openedx()
        print("Deadlines from Open edX:", deadlines)
        print("REMINDER_DAYS:", REMINDER_DAYS)
    else:
        deadlines = load_json_file("deadlines.json")
    sent_reminders = load_json_file("sent_reminders.json")
    upcoming_deadlines = []
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    for item in deadlines:
        due_date = datetime.strptime(item["due_date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        days_left = (due_date - today).days
        if 1 <= days_left <= 3:
            priority = "high"
            emoji = "🔴"
        elif 4 <= days_left <= 7:
            priority = "normal"
            emoji = "🟡"
        elif days_left == 0:
            priority = "urgent"
            emoji = "🚨"
        else:
            priority = "low"
            emoji = "🟢"
        print("Priority:", priority)
        print("Emoji:", emoji)
        reminder_id = f"{item['course']}_{item['assignment']}_{item['due_date']}"
        if 0 <= days_left <= REMINDER_DAYS and reminder_id not in sent_reminders:
            message = format_deadline_message(
                item,
                days_left,
                emoji,
                priority
            )
            upcoming_deadlines.append(message)
            sent_reminders.append(reminder_id)

    if upcoming_deadlines:
        message_text = "⚠️ Upcoming Deadline Reminder\n\n" + "\n".join(upcoming_deadlines)
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "⚠️ Upcoming Deadline Reminder"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_text
                    }
                }
            ]
        }
        try:
            send_slack_message(webhook_url, message)
            with open("sent_reminders.json", "w") as file:
                json.dump(sent_reminders, file, indent=4)
        except Exception as error:
            print("Slack sending failed:", error)
    else:
        print("No upcoming deadlines.")
    write_log(
        f"Source: {'Open edX' if USE_OPENEDX else 'JSON'} | "
        f"Upcoming reminders: {len(upcoming_deadlines)}"
    )
if len(sys.argv) > 1:
    mode = sys.argv[1]
    if mode == "test":
        check_deadlines()
    elif mode == "run":
        check_deadlines()
        start_scheduler(CHECK_TIME, check_deadlines)
    else:
        print("Invalid mode. Use: test or run")
else:
    print("Usage: python main.py [test|run]")