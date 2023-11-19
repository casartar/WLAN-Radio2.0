# WLAN-Radio2.0

1. Komponenten
2. Zusammenbau
3. Software-Installation

## 1. Komponenten
TBD

## 2. Zusammenbau
TBD

## 3. Software-Installation

### Erstellen der SD-Karte für den Raspberry Pi mittels Raspberry Pi Imager

3.1. Raspberry Pi Imager installieren - https://www.raspberrypi.com/software/ <screenshot rpi-imager>

3.2. Betriebssystem auf SD Karte schreiben

  3.2.1. Pi Modell auswählen (Pi Zero WH) <screenshot>
  
  3.2.2. Raspberry Pi OS (Legacy) Lite auswählen <screenshot>
  
  3.2.3. Optionen setzen: 
* wlan ssid: radio
* passwort:12345678
* user:pi
* passwort:raspberry
* weitere optionen: nur "ssh per passwort" auswählen, sonst nix ändern

  3.2.4. SD Karte programmieren
  
### SD Karte in Raspi stecken und den Pi booten, warten, der erste Start dauert u.U. mehrere Minuten

### System aktualisieren
IP Adresse herausfinden

Verbinden per ssh, user: pi; passwort wie oben konfiguriert.
Der Befehl funktioniert unter Linux und unter Window in der PowerShell

```
ssh pi@xxx.xxx.xxx.xxx

sudo apt update
sudo apt upgrade
```

### GIT und Repo installieren

```
sudo apt install git
sudo git clone https://github.com/casartar/WLAN-Radio2.0.git
```

### LCD Komponenten installieren und Testen

```
sudo apt install i2c-tools
sudo apt install python3-pip
pip install RPLCD --break-system-packages
```

/boot/config.txt anpassen mit

```
sudo nano /boot/config.txt
```

Parameter: **dtparam=i2c_arm=on** einkommentieren

Speichern mit Strg+O und Schließen mit Strg+X und Enter.

Neustart

```
sudo reboot
```

Verbinden per ssh

```
cd ~/WLAN-Radio2.0/Software
python3 lcd_test.py
```

Auf dem LCD sollte jetzt **"WLAN Radio"** und **"1234567890abcdef"** angezeigt werden.

### 3.7. Audio Komponenten installieren und Testen

/boot/config.txt anpassen mit

```
sudo nano /boot/config.txt
```

Am Ende der Datei hinzufügen: **dtoverlay=hifiberry-dac**
Zeile auskommentieren (Raute vorne dran) **#dtparam=audio=on**
Zeile auskommentieren (Raute vorne dran)  **#dtoverlay=vc4-kms-v3d**

Speichern mit Strg+O und Schließen mit Strg+X und Enter.

Neustart

```
sudo reboot
```

Verbinden per ssh

Testen mit:

```
speaker-test -t wav -c 2
```

Es sollte "Front Left" und "Front Right" aus dem entsprechenden Lautsprecher ertönen.

### 3.8. MPD und MPC einrichten (Music Player Daemon, Music Player Client)

```
sudo apt install mpd
sudo apt install mpc
```

/etc/mpd.conf anpassen mit

```
sudo nano /etc/mpd.conf
```

Zeile ändern von
```
playlist_directory   /var/lib/mpd/playlists
```
in
```
playlist_directory   /home/pi/Playlists/
```

und 

```
audio_output {
#       type            "alsa"
#       name            "My ALSA Device"
#       device          "hw:0,0"        # optional
#       mixer_type      "hardware"      # optional
#       mixer_device    "default"       # optional
#       mixer_control   "PCM"           # optional
#       mixer_index     "0"             # optional
}
```
ändern in 

```
audio_output { 
        type            "alsa" 
        name            "sysdefault:CARD=sndrpihifiberry" 
        mixer_type      "software" 
}
```

Speichern mit Strg+O und Schließen mit Strg+X und Enter.

Das Verzeichnis anlegen: 
```
mkdir ~/Playlists
```

Default Playlist aus dem Repo in dieses Verzeichnis kopieren: 

```
cp ~/WLAN-Radio2.0/Playlist/Playlist.m3u Playlists/
```

mpd.service neu starten: 
```
sudo systemctl restart mpd
```
Testen ob Radio abgespielt wird
```
mpc load Playlist
mpc play
mpc next
mpc status
```
Wenn nach mpc load P Playlist nicht autovervollständigt wird, muss evtl. in der mpd.conf der User von mpd zu pi geändert werden.

MPD Library installieren
```
sudo apt install python3-mpd
```
MPD Test Script ausführen
```
cd ~/WLAN-Radio2.0/Software
python3 mpd_test.py
```







