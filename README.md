# Deadline Reminder SlackBot

Python-based Slack reminder bot for Team Foxtrot's German UDS Coding Camp I capstone project.

## Official Task Context

The selected capstone task was **Task 4: Deadline Reminder SlackBot**. The task asked for a Slack bot that checks the Open edX API for upcoming deadlines and sends notifications. The brief also noted that Open edX API access may involve OAuth complexity and that no local Open edX installation is required.

## Current MVP

The current stable MVP demonstrates the reminder workflow with JSON-based deadline data:

1. load deadline data,
2. calculate how close each deadline is,
3. assign a priority,
4. format a Slack reminder,
5. send the reminder through Slack.

Open edX integration has been explored and partially prepared, but the demonstrated stable workflow currently uses JSON data.

## Features

- Python reminder workflow
- JSON-based deadline data for the MVP
- Slack Incoming Webhook notification
- Combined reminder messages
- Environment variable configuration through `.env`
- Modular helpers for data loading, Slack sending, formatting, logging, and scheduling
- Open edX authentication/API preparation for future integration

## Project Structure

```text
main.py           Main workflow and command modes
config.py         Loads environment variables and settings
data_loader.py    Safely loads JSON files
slack_client.py   Sends Slack messages
utils.py          Formats reminder messages and priorities
scheduler.py      Runs reminder checks on a schedule
logger.py         Writes execution logs
auth.py           Open edX authentication preparation
openedx_api.py    Open edX deadline retrieval preparation
deadlines.json    Sample MVP deadline data
test_deadlines.py Deadline logic tests
```

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file locally. Do not commit it.

```text
SLACK_WEBHOOK_URL=your_slack_webhook_url
REMINDER_DAYS=3
CHECK_TIME=09:00
USE_OPENEDX=False

# Future Open edX integration
OPENEDX_BASE_URL=https://open.uds-staging-test.abzt.de
OPENEDX_CLIENT_ID=your_client_id
OPENEDX_CLIENT_SECRET=your_client_secret
```

## Run

Test one reminder check:

```bash
python main.py test
```

Run with the scheduler:

```bash
python main.py run
```

## Security Notes

- Do not hardcode Slack webhooks or OAuth secrets in Python files.
- Store secrets in `.env`.
- Keep `.env` out of Git with `.gitignore`.
- Do not submit or share `.env` files in zip uploads.

## Open edX Integration Status

The target final product should retrieve live deadlines from Open edX. The project currently includes preparatory Open edX authentication/API files, but the stable demonstrated MVP uses JSON.

Recommended next steps for Open edX integration:

1. confirm OAuth client credentials on staging,
2. request a bearer token from the Open edX OAuth endpoint,
3. call course APIs for the Team Foxtrot test course,
4. extract due-date information,
5. replace JSON deadline data with live API results.

## Known Limitations

- The current MVP uses JSON instead of live Open edX deadline data.
- Open edX OAuth/API integration still needs final validation.
- Tests should remain date-independent.
- Production deployment, stronger logging, and monitoring are future improvements.

## Roadmap

1. Stabilize MVP date parsing and tests.
2. Complete Open edX token and course API validation.
3. Retrieve live deadline data from Open edX.
4. Deploy the scheduler on a server or cloud environment.
5. Add user-specific reminders and stronger logging.

## AI and Source Disclosure

AI support may be used for debugging explanations, documentation structure, and presentation wording under the AI Assessment Scale. Any copied or adapted code from external tutorials, prior teams, Stack Overflow, or AI tools should be disclosed in the lab report and presentation materials.
