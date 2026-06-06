import requests
from auth import get_access_token
from config import OPENEDX_BASE_URL
def get_deadlines_from_openedx():
    token = get_access_token()
    if not token:
        print("No Open edX token available.")
        return []
    headers = {
        "Authorization": f"JWT {token}"
    }
    TARGET_COURSE_ID = "course-v1:GermanUDS+Task4-Foxtrot+2026_Q2"
    deadlines = []
    print(f"\nFetching target course: {TARGET_COURSE_ID}")
    course_url = f"{OPENEDX_BASE_URL}/api/courses/v1/courses/{TARGET_COURSE_ID}"
    course_response = requests.get(course_url, headers=headers)
    if course_response.status_code != 200:
        print(f"Failed to fetch target course. Status: {course_response.status_code}")
        return []
    course_data = course_response.json()
    course_name = course_data.get("name", "Unknown Course Name")
    print(f"Successfully found: {course_name}")
    dates_url = f"{OPENEDX_BASE_URL}/api/course_home/v1/dates/{TARGET_COURSE_ID}"
    dates_response = requests.get(dates_url, headers=headers)
    print("Dates API status:", dates_response.status_code)
    if dates_response.status_code == 200:
        dates_data = dates_response.json()
        if "course_date_blocks" in dates_data:
            for block in dates_data["course_date_blocks"]:
                if block.get("date_type") == "assignment-due-date":
                    deadlines.append({
                        "course": course_name,
                        "assignment": block.get("title") or block.get("description", "Assignment"),
                        "due_date": block.get("date"),
                        "priority": "normal"
                    })
    print(f"\nDeadlines found: {len(deadlines)}")
    return deadlines
if __name__ == "__main__":
    final_deadlines = get_deadlines_from_openedx()
    for d in final_deadlines:
        print(d)