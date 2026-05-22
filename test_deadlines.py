from datetime import datetime


def is_upcoming_deadline(due_date, reminder_days):
    today = datetime.today()

    due_date = datetime.strptime(due_date, "%Y-%m-%d")

    days_left = (due_date - today).days

    return 0 <= days_left <= reminder_days


assert is_upcoming_deadline("2026-05-25", 10) == True
assert is_upcoming_deadline("2026-05-19", 10) == False
assert is_upcoming_deadline("2026-06-30", 10) == False

print("All tests passed successfully.")