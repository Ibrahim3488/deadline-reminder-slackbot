import json
from argparse import REMAINDER
from datetime import date, datetime
from email import message
from token import TYPE_COMMENT
from urllib import response


import requests
from dotenv import load_dotenv
from pathlib import Path
import os

from pathlib import Path
from dotenv import dotenv_values

from pathlib import Path
from dotenv import dotenv_values

from pathlib import Path
from dotenv import dotenv_values

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL")

with open("deadlines.json", "r") as file:
    deadlines = json.load(file)
"""def get_deadline_from_file():
    with open("deadline.json", "r") as file:
        return json.load(file)
    
def get_deadlines_from_lms():
    #todo:Later replace this with real open edX API call
    #Example:
    #response = requests.get(lms_api_url, headers=headers)
    #:return response.json()
    pass
#for now use fake json data
deadlines = get_deadline_from_file()"""
#later change only this line
#deadline = get_deadlines_from_lms()
deadline = [
    {
        "course": "Python Basics",
        "assigment":"Unit Testing Lab",
        "deu_date": "2026-05-15"
    },
    {
        "course": "Cybersecurity",
        "assigment":"Final presentation",
        "deu_date": "2026-05-20"
    },
    {
        "course": "Complexity Problem solving",
        "assigment":"Mid Term Exam",
        "deu_date": "2026-7-24"
    }
]
today = datetime.today()

for item in deadline:
    due_date = datetime.strptime(item['deu_date'], "%Y-%m-%d")
    days_left = (due_date - today).days
    if days_left <= 3:

      message = {
         "text": f"""
         Upcoming Deadline
         course : {item["course"]}
         assigment : {item["assigment"]}
         deu_date : {item["deu_date"]}
        """
     }

#message = {"text": "Hello from my Deadline Reminder Bot"}

response = requests.post(webhook_url, json=message)
print(response.status_code)
print(response.text)