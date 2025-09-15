# IP_Updater

This basic python script helps keep services running within networks that lack a static IP address. This may include websites, media servers and other services. 

It works by polling https://api.ipify/ at regular intervals and comparing the result to an IP stored in a file. If a change is detected the file is update and a series of scripts are executed. Presently there's only one script for updating cloudflare DNS records, but more scripts may be added as and when i need them, feel free to submit a PR if you wish to make any improvements or add your own scripts.

## Usage

The usage of this script should hopefully be fairly simple, you can populate the .env with your preferences (but there are hopefully sensible defaults) and then run the script on your server or machine as you like. I primarily work with linux and as such a systemd service file is included in this repo, alongside a bash file for execution through screen or similar.

## Scripts
As previously mentioned there is currently only one script, for updating cloudflare DNS records. Docs for that are [here](scripts/update_cloudflare/README.md)

## Running as systemd service

To run this script as a systemd service, open the ip-setter.service file and replace ``<repo path>`` on lines 7 & 8 with the path of the repo on your server. Then copy this into systemd directory with the command
```sh
cp ./ip-setter.service /etc/systemd/system/
``` 

Then you can start/enable the service as you would any other.