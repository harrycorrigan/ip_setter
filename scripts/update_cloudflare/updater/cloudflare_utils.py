"""
Basic utilities for interacting with cloudflare DNS records
"""

import traceback
import requests
import json


def get_endpoint(route: str, key: str) -> dict:
    return requests.get(
        f"https://api.cloudflare.com/{route}",
        headers={"Authorization": f"Bearer {key}"},
    ).json()


def update_endpoint(route: str, bearer_token: str, data: dict) -> dict:
    return requests.patch(
        f"https://api.cloudflare.com/{route}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        data=json.dumps(data),
    ).json()


def get_dns_records(bearer_token: str, zone_id: str) -> list[dict]:
    return get_endpoint(f"client/v4/zones/{zone_id}/dns_records", bearer_token)[
        "result"
    ]


def get_dns_record_value(bearer_token: str, zone_id: str, record_name: str):
    records = get_dns_records(bearer_token, zone_id)

    for record in records:
        if record_name == record["name"]:
            return record["id"], record["content"]
    raise Exception("Failed to find record with name '%s'" % (record_name))


def set_dns_record_value(bearer_token: str, zone_id: str, dns_rec_id: str, new_ip: str):
    try:
        return update_endpoint(
            f"client/v4/zones/{zone_id}/dns_records/{dns_rec_id}",
            bearer_token,
            {"content": new_ip},
        )["success"]
    except Exception as e:
        traceback.print_exception(e)
        return False
