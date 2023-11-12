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
3.3. SD Karte in Raspi stecken und den booten, warten, der erste Start dauert u.U. mehrere Minuten
3.4. IP Adresse im ztl-iot Netz finden
3.5. Verbinden per ssh, user: pi; passwort wie oben vorgegeben
3.6. System aktualisieren
3.6.1. sudo apt update
3.6.2. sudo apt upgrade
3.6.3 booten

3.7. GIT und Repo installieren
3.7.1. Verbinden per ssh
3.7.2. git installieren 
* sudo apt install git
3.7.3. Repo clonen
* sudo git clone https://github.com/casartar/WLAN-Radio2.0.git

3.8. LCD Komponenten installieren und Testen
3.8.1. sudo apt install i2c-tools
3.8.2. /boot/config.txt anpassen
3.8.2.1. Parameter: dtparam=i2c_arm=on einkommentieren
3.8.3. Booten
3.8.4. Verbinden per ssh
3.8.5. ... TBC

3.9. Audio Komponenten installieren und Testen
3.9.1. /boot/config.txt anpassen
3.9.1.1. sudo nano /boot/config.txt
3.9.1.2. Am Ende der Datei hinzufügen: dtoverlay=hifiberry-dac
3.9.1.3. Zeile auskommentieren (Raute vorne dran) #dtparam=audio=on
3.9.1.4. Zeile auskommentieren (Raute vorne dran)  #dtoverlay=vc4-kms-v3d
3.9.1.5. speichern, nano verlassen
3.9.2. Booten
3.9.3. Verbinden per ssh
3.9.4. Testen mit: speaker-test -t wav -c 2

3.10. MPD und MPC einrichten (Music Player Daemon, Music Player Client)
3.10.1. sudo apt install mpd
3.10.2. sudo apt install mpc 
3.10.3. /etc/mpd.conf anpassen
3.10.3.1. sudo nano /etc/mpd.conf
3.10.3.2. Zeile ändern 
* von **"playlist_directory   /var/lib/mpd/playlists"**
* in **"playlist_directory   /home/pi/Playlists/"**
3.10.3.3. Die Zeilen für "audio_output{}" EINkommentieren und ändern, siehe unten
3.10.3.4. Den User für mpd ändern: Zeile "user mpd" ändern in "user pi".
3.10.3.5. nano Editor verlassen
3.10.4. Das Verzeichnis anlegen: mkdir Playlists
3.10.5. Default Playlist aus dem Repo in dieses Verzeichnis kopieren: cp WLAN-Radio2./Playlist/Playlist.m3u Playlists/
3.10.6. mpd.service neu starten: "sudo systemctl restart mpd"


### /etc/mpd.conf vor Änderung
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

### /etc/mpd.conf nach Änderung

```
audio_output { 
        type            "alsa" 
        name            "sysdefault:CARD=sndrpihifiberry" 
        mixer_type      "software" 
}
```






