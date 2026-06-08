from datetime import datetime, timedelta
import unittest


def is_upcoming_deadline(due_date, reminder_days):
    today = datetime.today()
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    days_left = (due_date - today).days
    return 0 <= days_left <= reminder_days


class DeadlineTests(unittest.TestCase):
    def test_deadline_within_reminder_window(self):
        due_date = (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        self.assertTrue(is_upcoming_deadline(due_date, 10))

    def test_past_deadline_is_not_upcoming(self):
        due_date = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        self.assertFalse(is_upcoming_deadline(due_date, 10))

    def test_deadline_outside_window_is_not_upcoming(self):
        due_date = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.assertFalse(is_upcoming_deadline(due_date, 10))


if __name__ == "__main__":
    unittest.main()
