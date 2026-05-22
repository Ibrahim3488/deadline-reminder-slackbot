import json
import os
import time
from datetime import datetime

import requests
import schedule
from dotenv import load_dotenv
from slack_client import send_slack_message
from data_loader import load_json_file
from utils import get_priority_emoji, format_deadline_message
from config import (
    webhook_url,
    USE_OPENEDX,
    REMINDER_DAYS,
    CHECK_TIME
)

def get_deadlines_from_openedx():
    # TODO: replace JSON data with real Open edX API response later
    pass


    # your logic here

def check_deadlines():

    #USE_OPENEDX = False  # Change to True later when Open edX API works

    if USE_OPENEDX:
        from openedx_api import get_deadlines_from_openedx
        deadlines = get_deadlines_from_openedx()

    else:
        deadlines = load_json_file("deadlines.json")

    sent_reminders = load_json_file("sent_reminders.json")

    today = datetime.today()
    upcoming_deadlines = []

    for item in deadlines:
        due_date = datetime.strptime(item["due_date"], "%Y-%m-%d")
        days_left = (due_date - today).days
        priority = item.get("priority", "normal")
        emoji = get_priority_emoji(priority)
        print("Priority:", priority)
        print("Emoji:", emoji)

        reminder_id = f"{item['course']}_{item['assignment']}_{item['due_date']}"
        #if 0 <= days_left <= 3 and reminder_id not in sent_reminders:
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
        """message = {
            "text": message_text
        }"""

        try:
            send_slack_message(webhook_url, message)

            with open("sent_reminders.json", "w") as file:
                json.dump(sent_reminders, file, indent=4)

        except Exception as error:
            print("Slack sending failed:", error)

    else:
        print("No upcoming deadlines.")

    #with open("bot.log", "a") as log:
       # log.write(f"{datetime.now()} - Reminder check completed\n")
    with open("bot.log", "a") as log:
        log.write(
            f"{datetime.now()} | "
            f"Source: {'Open edX' if USE_OPENEDX else 'JSON'} | "
            f"Upcoming reminders: {len(upcoming_deadlines)}\n"
        )

check_deadlines()

#schedule.every().day.at("09:00").do(check_deadlines)
#schedule.every(1).minutes.do(check_deadlines)
schedule.every().day.at(CHECK_TIME).do(check_deadlines)
while True:
    schedule.run_pending()
    time.sleep(60)