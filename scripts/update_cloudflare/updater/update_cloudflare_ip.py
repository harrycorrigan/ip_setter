import os
import dotenv
from . import cloudflare_utils as cloudflare


def update(
    new_ip: str,
    cf_email: str,
    cf_global_key: str,
    cf_zone_id: str,
    ignore_names: list[str] = [],
):
    try:
        for record in cloudflare.get_dns_records(cf_email, cf_global_key, cf_zone_id):
            if record["type"] != "A":
                continue
            if record["content"] == new_ip:
                continue
            if record["name"] in ignore_names:
                continue

            print(
                "SCRIPT NOTICE (CLOUDFLARE_UPDATER): Updating DNS Record, name %s, curr value %s, new value %s"
                % (record["name"], record["content"], new_ip)
            )

            cloudflare.set_dns_record_value(
                cf_email, cf_global_key, cf_zone_id, record["id"], new_ip
            )
    except TypeError:
        print("SCRIPT ERROR (CLOUDFLARE_UPDATER): Failed to get DNS records. Are your credentials correct?")


def entry(old_ip: str, new_ip: str):
    # get .env from parent directory
    dotenv_path = ("/".join(__file__.replace("\\", "/").split("/")[:-2])) + "/.env"

    dotenv.load_dotenv(dotenv_path)
    try:
        CF_EMAIL = os.environ["CF_EMAIL"]
        CF_GLOBAL_KEY = os.environ["CF_GLOBAL_KEY"]
        CF_ZONE_ID = os.environ["CF_ZONE_ID"]
        IGNORED_RECORDS = os.environ.get("IGNORE_DNS_RECORD_NAMES", "").split(",")
    except KeyError:
        print(
            "SCRIPT ERROR (CLOUDFLARE_UPDATER): Keys missing from .env at path (%s). Did you copy the template.env?"
            % (dotenv_path)
        )

        return
    update(new_ip, CF_EMAIL, CF_GLOBAL_KEY, CF_ZONE_ID, ignore_names=IGNORED_RECORDS)
