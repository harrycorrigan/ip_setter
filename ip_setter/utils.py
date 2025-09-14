import traceback


def print_exception(e: Exception):
    exc_str = traceback.format_exception(e)
    print("\n".join(exc_str))
    # print line under formatted exception for ease of reading
    print("-" * max(len(s) for s in exc_str))
