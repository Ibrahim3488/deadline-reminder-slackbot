import json
import os
import time
from datetime import datetime

import requests
import schedule
from dotenv import load_dotenv


load_dotenv()
webhook_url = os.getenv("SLACK_WEBHOOK_URL")

USE_OPENEDX = os.getenv("USE_OPENEDX", "False") == "True"
REMINDER_DAYS = int(os.getenv("REMINDER_DAYS", 3))
CHECK_TIME = os.getenv("CHECK_TIME", "09:00")

def get_deadlines_from_openedx():
    # TODO: replace JSON data with real Open edX API response later
    pass


def check_deadlines():

    #USE_OPENEDX = False  # Change to True later when Open edX API works

    if USE_OPENEDX:
        from openedx_api import get_deadlines_from_openedx
        deadlines = get_deadlines_from_openedx()

    else:
        try:
            with open("deadlines.json", "r") as file:
                deadlines = json.load(file)

        except FileNotFoundError:
            print("deadlines.json file not found")
            deadlines = []

        except json.JSONDecodeError:
            print("Invalid JSON format in deadlines.json")
            deadlines = []

    try:
        with open("sent_reminders.json", "r") as file:
            sent_reminders = json.load(file)

    except FileNotFoundError:
        print("sent_reminders.json file not found")
        sent_reminders = []

    except json.JSONDecodeError:
        print("Invalid JSON format in sent_reminders.json")
        sent_reminders = []

    today = datetime.today()
    upcoming_deadlines = []

    for item in deadlines:
        due_date = datetime.strptime(item["due_date"], "%Y-%m-%d")
        days_left = (due_date - today).days
        priority = item.get("priority", "normal")
        if priority == "high":
            emoji = "🔴"
        else:
            emoji = "🟡"
        print("Priority:", priority)
        print("Emoji:", emoji)

        reminder_id = f"{item['course']}_{item['assignment']}_{item['due_date']}"
        #if 0 <= days_left <= 3 and reminder_id not in sent_reminders:
        if 0 <= days_left <= REMINDER_DAYS and reminder_id not in sent_reminders:
            upcoming_deadlines.append(
                f"{emoji} PRIORITY: {priority.upper()}\n"
                f"📘 Course: {item['course']}\n"
                f"📝 Assignment: {item['assignment']}\n"
                f"📅 Due in: {days_left} day(s)\n"
            )
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
        """message = {
            "text": message_text
        }"""

        try:
            response = requests.post(webhook_url, json=message)
            print(response.status_code, response.text)

            with open("sent_reminders.json", "w") as file:
                json.dump(sent_reminders, file, indent=4)

        except Exception as error:
            print("Slack sending failed:", error)

    else:
        print("No upcoming deadlines.")

    with open("bot.log", "a") as log:
        log.write(f"{datetime.now()} - Reminder check completed\n")

check_deadlines()

#schedule.every().day.at("09:00").do(check_deadlines)
#schedule.every(1).minutes.do(check_deadlines)
schedule.every().day.at(CHECK_TIME).do(check_deadlines)
while True:
    schedule.run_pending()
    time.sleep(60)