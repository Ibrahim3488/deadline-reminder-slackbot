def get_priority_emoji(priority):
    if priority == "high":
        return "🔴"

    return "🟡"


def format_deadline_message(item, days_left, emoji, priority):
    return (
        f"{emoji} PRIORITY: {priority.upper()}\n"
        f"📘 Course: {item['course']}\n"
        f"📝 Assignment: {item['assignment']}\n"
        f"📅 Due in: {days_left} day(s)\n"
    )