import schedule
import time


def start_scheduler(check_time, job_function):

    schedule.every().day.at(check_time).do(job_function)

    while True:
        schedule.run_pending()
        time.sleep(60)