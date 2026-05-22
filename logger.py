from datetime import datetime


def write_log(message):

    with open("bot.log", "a") as log:
        log.write(f"{datetime.now()} | {message}\n")