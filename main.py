import json
import os
import time
from datetime import datetime

import requests
import schedule
from dotenv import load_dotenv


load_dotenv()
webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def get_deadlines_from_openedx():
    # TODO: replace JSON data with real Open edX API response later
    pass


def check_deadlines():
    with open("deadlines.json", "r") as file:
        deadlines = json.load(file)

    with open("sent_reminders.json", "r") as file:
        sent_reminders = json.load(file)

    today = datetime.today()
    upcoming_deadlines = []

    for item in deadlines:
        due_date = datetime.strptime(item["due_date"], "%Y-%m-%d")
        days_left = (due_date - today).days

        reminder_id = f"{item['course']}_{item['assignment']}_{item['due_date']}"

        if 0 <= days_left <= 3 and reminder_id not in sent_reminders:
            upcoming_deadlines.append(
                f"• {item['course']} - {item['assignment']} is due in {days_left} day(s)"
            )
            sent_reminders.append(reminder_id)

    if upcoming_deadlines:
        message_text = "⚠️ Upcoming Deadline Reminder\n\n" + "\n".join(upcoming_deadlines)

        message = {
            "text": message_text
        }

        try:
            response = requests.post(webhook_url, json=message)
            print(response.status_code, response.text)

            with open("bot.log", "a") as log:
                log.write(f"{datetime.now()} - Slack message sent successfully\n")

        except Exception as error:
            print("Slack sending failed:", error)

            with open("bot.log", "a") as log:
                log.write(f"{datetime.now()} - Slack sending failed: {error}\n")

        with open("sent_reminders.json", "w") as file:
            json.dump(sent_reminders, file, indent=4)
    else:
        print("No upcoming deadlines.")
    with open("bot.log", "a") as log:
        log.write(f"{datetime.now()} - Reminder check completed\n")


check_deadlines()

schedule.every().day.at("09:00").do(check_deadlines)

while True:
    schedule.run_pending()
    time.sleep(60)