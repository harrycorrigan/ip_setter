import requests
import time
from .utils import print_exception


def get_wan_addr(retry_delay_base=10, max_wait_time=300) -> str:
    fail_count = 0

    while True:
        try:
            return requests.get("https://api.ipify.org/").text
        # catch known exceptions to print appropriate message
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            print("ERROR: Network Error, Connection Lost....")
        # anything unexpected is logged
        except Exception as e:
            print("ERROR: Unknown exception")
            print_exception(e)
        fail_count += 1

        # linearly scale wait time relative to amount of failures if failed more then 3 times
        wait_time = (
            retry_delay_base
            # this is an arbitrary value
            if fail_count < 3
            else min(max_wait_time, fail_count * retry_delay_base)
        )

        print("Failed %s times, retrying in %ss" % (fail_count, wait_time))
        time.sleep(wait_time)
