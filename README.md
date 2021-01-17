# Music Box

Use an Orange Pi PC Plus as a kid's music player

## Dependencies
* sudo pip3 install OrangePi.GPIO
* sudo apt install sox libsox-fmt-all

We're using https://github.com/Jeremie-C/OrangePi.GPIO because it implements pull-up/down and OPi.GPIO library doesn't

# Setup:
Add User to Groups:

`sudo usermod -a -G audio orangepi`

Make sure audio is set to output from line out and not hdmi:

`pacmd set-default-sink 0`

## Run automatically

Because the GPIO library needs root priviledges, add this as a cron-job for root: `sudo crontab -e`:
```
@reboot /usr/bin/python3 /home/orangepi/musicbox/musicbox.py
```

## Normalize music
Normalize tracks so volumes are relatively the same
```
sudo apt install normalize-audio
normalize-audio -m *
```