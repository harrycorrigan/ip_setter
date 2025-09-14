import time

from .utils import print_exception


def get_saved_ip(file_location: str):
    try:
        with open(file_location, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        return ""
    except Exception as e:
        # capture any odd errors that may be a result of multiple instances running at the same time or otherwise
        print("ERROR: Exception raised when reading IP file %s" % (file_location))
        print_exception(e)
        return ""


def save_ip(file_location: str, ip: str):
    try:
        with open(file_location, "w") as f:
            f.write(ip)
    except Exception as e:
        # capture any odd errors that may be a result of multiple instances running at the same time or otherwise
        print("ERROR: Exception raised when saving IP to file %s" % (file_location))
        print_exception(e)
        print("Retrying in 5s")
        time.sleep(5)
        save_ip(file_location, ip)
