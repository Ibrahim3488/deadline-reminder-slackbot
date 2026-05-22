# Deadline Reminder SlackBot

A Python-based Slack bot that sends automated deadline reminders to a Slack channel.

## Features

- Reads deadline data from a JSON file
- Sends reminders to Slack using Incoming Webhooks
- Calculates upcoming deadlines
- Uses environment variables for secure webhook management
- GitHub-integrated project

## Technologies Used

- Python
- Slack Incoming Webhooks
- Requests library
- JSON
- Git & GitHub
- python-dotenv

## Project Structure

```text
DeadlineReminder/
│
├── main.py
├── deadlines.json
├── .env
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Ibrahim3488/deadline-reminder-slackbot.git
```

Go to project folder:

```bash
cd deadline-reminder-slackbot
```

Install dependencies:

```bash
pip install requests python-dotenv
```

## Configure Slack Webhook

Create a `.env` file:

```text
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

## Run the Bot

```bash
python main.py
```

## Example Slack Notification

```text
⚠️ Upcoming Deadline

Course: Python Basics
Assignment: Unit Testing Lab
Due in: 2 day(s)
```

## Future Improvements

- Connect to Open edX API
- Automatic scheduled execution
- Multiple Slack channels
- User-specific reminders
- Database integration

## Author

Features
Architecture
Project Structure
Future Improvements
Open edX Integration Status

main.py → reminder workflow
auth.py → Open edX authentication
openedx_api.py → Open edX API requests
deadlines.json → local mock data
sent_reminders.json → duplicate prevention
bot.log → execution logs

Open edX sandbox authentication endpoint was reachable,
but sandbox did not return JWT token data.
Project currently uses local JSON mock data until
real API credentials/access are available.

## Slack Message Formatting

The bot uses Slack Block Kit to display reminders in a structured format with headers, dividers, and formatted sections.
## Installation

```bash
git clone <repository-url>
cd deadline-reminder-slackbot

pip install -r requirements.txt
```

## Code Structure Improvement

The project uses reusable helper functions such as `format_deadline_message()` to keep the code clean, readable, and maintainable.

## Updated Architecture: scheduler.py Added

`scheduler.py` was added to separate the automatic scheduling logic from `main.py`.

### Purpose of scheduler.py

`scheduler.py` is responsible for:
- starting the daily reminder schedule,
- running the reminder function at the configured time,
- keeping the bot active continuously.

### Updated File Responsibilities

```text
.env
  ↓
config.py
  ↓
main.py  ← main workflow controller
  ↓
scheduler.py  ← runs check_deadlines() automatically
  ↓
Slack reminders
