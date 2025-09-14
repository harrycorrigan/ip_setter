"""
Contains functions for actually executing scripts. New scripts should be added here.

"""

from .update_cloudflare import entry as cf_updater


def execute_python_scripts(old_ip: str, new_ip: str):
    # i was going to do this dynamically by traversing the directory tree
    # but with folders that got increasingly complex so i decided to leave it out in favour of simplicity
    cf_updater.entry(old_ip, new_ip)
