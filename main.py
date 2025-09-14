import os
import time

import dotenv
from ip_setter import save_ip, get_saved_ip, get_wan_addr
from ip_setter.utils import print_exception

from scripts.execute_scripts import execute_python_scripts

# get .env as sibling
dotenv_path = ("/".join(__file__.replace("\\", "/").split("/")[:-1])) + "/.env"

dotenv.load_dotenv(dotenv_path)

try:
    API_BASE_RETRY_DELAY = int(os.environ["API_BASE_RETRY_DELAY"])
    API_POLL_RATE_SECONDS = int(os.environ["API_POLL_RATE_SECONDS"])
    IP_FILE = os.environ["IP_FILE_PATH"]
    DEBUG = bool(os.environ.get("DEBUG", 0))
except (KeyError, ValueError):
    print(
        "ERROR: Invalid .env (%s) configuration, please adjust & try again"
        % (dotenv_path)
    )
    exit()


def on_ip_change(old_ip: str, curr_ip: str):
    save_ip(IP_FILE, curr_ip)
    try:
        execute_python_scripts(old_ip, curr_ip)
    except Exception as e:
        print("NOTICE: Error in script(s) execution")
        print_exception(e)


def do_ip_loop():
    while True:
        # reload IP on every iteration, this creates a more robust program in cases of
        # write errors, shutdowns or otherwise.
        saved_ip = "" if DEBUG else get_saved_ip(IP_FILE)
        curr_ip = get_wan_addr(retry_delay_base=API_BASE_RETRY_DELAY)
        if curr_ip != saved_ip:
            print(
                "NOTICE: IP change detected, %s -> %s, saving..." % (saved_ip, curr_ip)
            )
            on_ip_change(saved_ip, curr_ip)
        time.sleep(API_POLL_RATE_SECONDS)


if __name__ == "__main__":
    while True:
        try:
            do_ip_loop()
        except KeyboardInterrupt:
            print("NOTICE: Keyboard interrupt received, quitting...")
            exit()
        except Exception as e:
            print("ERROR: Exception in main loop.")
            print_exception(e)
            print("NOTICE: Restarting...")
