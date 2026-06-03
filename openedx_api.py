import requests
from auth import get_access_token
from config import OPENEDX_BASE_URL
import datetime

from config import OPENEDX_BASE_URL
print("OPENEDX_API FILE LOADED")
print("BASE URL =", OPENEDX_BASE_URL)
print("OPENEDX_API FILE LOADED")
print("CURRENT TIME:", datetime.datetime.now())
def get_deadlines_from_openedx():
    print(">>> RUNNING openedx_api.py")

    token = get_access_token()

    print("Token length:", len(token) if token else 0)
    print("Token preview:", token[:30] if token else "None")

    if not token:
        print("No Open edX token available.")
        return []

    headers = {
        "Authorization": f"JWT {token}"
    }
    courses_url = f"{OPENEDX_BASE_URL}/api/courses/v1/courses/"

    print("Courses URL:", courses_url)
    print("COURSES URL:", courses_url)
    response = requests.get(courses_url, headers=headers)

    print("Courses status:", response.status_code)

    if response.status_code != 200:
        print("Failed to fetch courses:", response.text)
        return []

    courses = response.json().get("results", [])

    print("Courses found:", len(courses))

    deadlines = []

    for course in courses:
        print("Course:", course.get("name"))
        print("Course ID:", course.get("id"))
        print("----------------")
        if course.get("name") != "test_date":
            continue
        print("Course:", course.get("name"))
        print("Course ID:", course.get("id"))


        blocks_url = course.get("blocks_url")

        print("Blocks URL:", blocks_url)

        #if not blocks_url:
            #continue
        course_id = course.get("id")

        dates_url = f"{OPENEDX_BASE_URL}/api/course_home/v1/dates/{course_id}"

        dates_response = requests.get(
            dates_url,
            headers=headers
        )

        print("Dates status:", dates_response.status_code)
        print("Dates response:", dates_response.text[:1000])
        """blocks_response = requests.get(
            blocks_url,
            headers=headers,
            params={
                "depth": "all",
                "requested_fields": "display_name,due,graded,format,lms_web_url",
                "username": "m-ibrahim"
            }
        )

        print("Blocks status:", blocks_response.status_code)
        print("Blocks error:", blocks_response.text)
        print("Contains due?", "due" in blocks_response.text)

        blocks_data = blocks_response.json()
        blocks = blocks_data.get("blocks", {})

        for block in blocks.values():
            due = block.get("due")

            if due:
                print("FOUND DUE DATE:", due)

                deadlines.append({
                    "course": course.get("name"),
                    "assignment": block.get("display_name"),
                    "due_date": due[:10],
                    "priority": "normal"
                })"""

    print("Deadlines found:", deadlines)

    return deadlines


if __name__ == "__main__":
    deadlines = get_deadlines_from_openedx()
    print("Deadlines:", deadlines)