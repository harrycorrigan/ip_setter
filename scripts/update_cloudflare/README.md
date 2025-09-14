# Cloudflare Updater Script

This is a basic script that on ``scripts/update_cloudflare/entry.py::entry(new_ip, old_ip)`` being called updates
all A records (outside of IGNORE_DNS_RECORD_NAMES environment variable) for a particular cloudflare domain. 

This is useful for self-hosted domains and services that may be running on a network with a dynamic IP address. 


## Usage

The script usage is fairly simple, it's called via ``scripts/execute_scripts.py`` which in turn is called by ``main.py`` when a IP address change is detected, all you need is the relevant information from cloudflare stored in a dotenv file.
There is a template dotenv available (``scripts/update_cloudflare/.env``), just fill in your credentials and zone id.


For more information on generating the tokens see cloudflare's own documentation (https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/)