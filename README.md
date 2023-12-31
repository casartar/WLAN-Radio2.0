# WLAN-Radio2.0

![alt](Doc/Images/rn_image_picker_lib_temp_afa1ddd7-56b1-41ca-871a-b3567bc09444-removebg-preview.png)

## 1. Komponenten
TBD

## Testaufbau
### SMD Bestückung
Siehe [ibom](https://github.com/casartar/WLAN-Radio2.0/blob/main/Hardware/WLAN-Radio-HAT/bom/ibom.html)
### THT Bestückung

Buchsenleiste an WLAN-Radio-HAT anlöten. Darauf auchten, dass der Stecker gut auf der Platine aufliegt.

![alt](Doc/Images/rn_image_picker_lib_temp_1d7d7d80-74f2-4d0a-b726-9af4aa6a0726.jpg)

Gewinkelte Stiftleisten anlöten.

Aus Gründen für die 5V Spannungsversorgung gerade Stiftleisten verwenden.

![alt](Doc/Images/rn_image_picker_lib_temp_fb06218b-076f-41ba-8c32-5e0aae7ec380.jpg)

Buchsenleiste and LCD anlöten.

![alt](Doc/Images/rn_image_picker_lib_temp_234642c8-5492-4c17-928f-5ccbc46bb605.jpg)

Gewinkelte Stifleisten an Verstärkermodul anlöten.

![alt](Doc/Images/rn_image_picker_lib_temp_0e6c855c-58bf-4a00-86e8-27c6f86bd6be.jpg)



### Testaufbau

* WLAN-Radio-HAT auf Raspberry Pi Zero W stecken.
* LCD anschließen.
* Verstärker anschließen.
* Lautsprecher an Verstärker anstecken.
* Micro-USB-Kabel an das Raspberry Pi anschließen (PWR IN).

![alt](Doc/Images/rn_image_picker_lib_temp_f6003c7c-b0ff-4a12-8b8e-d8390baf359f.jpg)

## Software-Installation

### Erstellen der SD-Karte für den Raspberry Pi mittels Raspberry Pi Imager

Raspberry Pi Imager installieren - https://www.raspberrypi.com/software/ 

Raspberry Pi Imager ausführen.
![alt](Doc/Images/Screenshot_20231121_200553.png)
Gerät wählen: Raspberry Pi Zero
![alt](Doc/Images/Screenshot_20231121_201224.png)
Os wählen: Raspberry Pi OS (other)
![alt](Doc/Images/Screenshot_20231121_201930.png)
Raspberry Pi OS (Legacy) Lite
![alt](Doc/Images/Screenshot_20231121_202151.png)
SD-Karte wählen.
![alt](Doc/Images/Screenshot_20231121_202421.png)
Next
![alt](Doc/Images/Screenshot_20231121_202535.png)
Einstellungen bearbeiten.
![alt](Doc/Images/Screenshot_20231121_202631.png)
* Hostname: individuell benennen.
* Benutzer: "pi"
* Passwort: "raspberry"
* SSID: geheim
* Passwort: geheim

Im Reiter "Dienste" kann man auch gerne seinen Public Key hinterlegen, muss aber nicht sein.
![alt](Doc/Images/Screenshot_20231121_202818.png)

Im Reiter "Dienste" SSH aktivieren und "Passwort zur Authentifizierung verwenden" auswählen. Wer weiß was er tut, kann man auch gerne seinen Public Key hinterlegen, muss aber nicht sein.
![alt](Doc/Images/image.png)

Speichern und Ja wählen und mit Ja bestätigen
![alt](Doc/Images/Screenshot_20231121_203328.png)
SD-Karte wird beschrieben.
![alt](Doc/Images/Screenshot_20231121_203419.png)
SD-Karte ist fertig beschrieben.
![alt](Doc/Images/Screenshot_20231121_203637.png)

SD-Karte in Pi einstecken und Micro-USB-Kabel an Laptop anschließen.
  
### Der erste Start des Pi dauert u.U. mehrere Minuten

### System aktualisieren
IP Adresse herausfinden

Verbinden per ssh, user: pi; passwort wie oben konfiguriert.
Der Befehl funktioniert unter Linux und unter Window in der PowerShell

```
ssh pi@xxx.xxx.xxx.xxx

sudo apt update
sudo apt upgrade
```

### GIT installieren und WLAN-Radio2.0 clonen

```
sudo apt install git
sudo git clone https://github.com/casartar/WLAN-Radio2.0.git
```

### LCD Komponenten installieren und Testen

```
sudo apt install i2c-tools
sudo apt install python3-pip
sudo apt install python3-smbus
pip install RPLCD
```
Wenn pip einen Fehler ausgibt noch mal versuchen mit:
```
pip install RPLCD --break-system-packages
```

/boot/config.txt anpassen mit

```
sudo nano /boot/config.txt
```

Parameter: **dtparam=i2c_arm=on** einkommentieren

Speichern mit Strg+O, Enter und Schließen mit Strg+X.

Neustart

```
sudo reboot
```

Verbinden per ssh

```
sudo i2cdetect -y 1
cd ~/WLAN-Radio2.0/Software
python3 lcd_test.py
```

Auf dem LCD sollte jetzt **"WLAN Radio"** und **"1234567890abcdef"** angezeigt werden.

### Audio Komponenten installieren und Testen

/boot/config.txt anpassen mit

```
sudo nano /boot/config.txt
```

Am Ende der Datei hinzufügen: **dtoverlay=hifiberry-dac**
Zeile auskommentieren (Raute vorne dran) **#dtparam=audio=on**
Zeile auskommentieren (Raute vorne dran)  **#dtoverlay=vc4-kms-v3d**

Speichern mit Strg+O, Enter und Schließen mit Strg+X.

Neustart

```
sudo reboot
```

Verbinden per ssh

Testen mit:

```
speaker-test -t wav -c 2
```

Es sollte "Front Left" und "Front Right" aus den entsprechenden Lautsprechern ertönen.

Mit Strg + C kann die Ausgabe abbrechen.

### MPD und MPC einrichten (Music Player Daemon, Music Player Client)

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

Speichern mit Strg+O, Enter und Schließen mit Strg+X.

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
mpc pause
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

Es sollte ein Sender abgespielt werden.

Mit Strg + C wird der test beendet.

### Radio Testen

```
cd ~/WLAN-Radio2.0/Software
python3 radio_test.py
```

Mit der Pinzette die beiden Pins für Next respektive Previous kurzschließen und prüfen, ob ein anderer Sender abgespielt wird.

### Weitere WLAN-Zugangsdaten hinzufügen

```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Die konfiguration sollte in etwa so aussehen:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
        ssid="HierKönnteIhreSsidStehen"
        psk=e04000a6ccb88f7ac28bd18ed807fdb820ac8524dbc6f50d4bfe2d788c3609fd
}
```

Das muss erweitert werden zu:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
        ssid="HierKönnteIhreSsidStehen"
        psk=e04000a6ccb88f7ac28bd18ed807fdb820ac8524dbc6f50d4bfe2d788c3609fd
}
network={
        ssid="AndereSsid"
        psk="pazzzW0rd"
}
```

Speichern mit Strg+O, Enter und Schließen mit Strg+X.

### Autostart

```
sudo cp ~/WLAN-Radio2.0/Config/wlan-radio.service /etc/systemd/system/
sudo chmod 640 /etc/systemd/system/wlan-radio.service
systemctl status wlan-radio
sudo systemctl daemon-reload
sudo systemctl enable wlan-radio
sudo systemctl start wlan-radio
sudo systemctl status wlan-radio
```

## Gehäuse Lasern

Benötigt wird die Datei Case_with_custom_cutouts_6mm.svg

Das Gehäuse wird aus Buche Sperrholzplatten 6mm gelasert. 
Startingpoint sind 80% Leistung und 20 mm/s Geschwindigkeit.

Nach dem Lasern sollten die Schnittkanten mit Schmiergelpapier bearbeitet werden, da das Holz sehr nach verbrannt riecht.

Ob man das Holz weiter bearbeiten, also einölen oder lackieren möchte, darf jeder selbst entscheiden.

## Fräsarbeiten

Die Bedienelemente müssen im Holz versenkt werden, da die Gewinde für 6 mm Holz zu kurz sind.
Für die Vertiefungen wird mit der Oberfräse 3 mm abgefäst.

Wo gefäst werden muss, ist in der Datei Deepenings.svg rot markiert.

ACHTUNG! Die Zeichung ist die Sicht von Außen auf das Radio, die Vertiefungen sind aber innen. Beim Display muss also gespiegelt ausgefräßt werden.

Am besten steckt man die Bauteile in die Aussparungen und zeichnet mit dem Bleistift an, wo gefräßt werden soll.

![alt](Doc/Images/rn_image_picker_lib_temp_5c200745-794b-4489-a20a-4eaecd2b725c.jpg)

![alt](Doc/Images/rn_image_picker_lib_temp_00bad2cb-d237-46a7-a9af-c1a5be741ca0.jpg)

## Einbau der Elektronik

### Rückwand (USB-C + Pi)
Vor dem einbau der USB-C Buchse werden an die Leitungen Dupont Buchsen gecrimpt.

Um den Pi zu montieren, müssen von außen vier Zylinderkopfschrauben M2,5 mit Länge 8 mm gesteckt werden.
Von innen werden Stehbolzen M2,5 (Länge relativ egal) mit Innen- und Außenewinde auf die Schrauben augeschraubt. Darauf wird der Pi gesteckt. Dann werden wieder vier Stehbolte mit Innen und Außengewinde aufgeschraubt. Länge 11 mm. Dann kommt der HAT und M2,5 Muttern.

### Deckel

An die beiden Taster werden zweipolige Stiftleisten gelötet und dann verschraubt.

Beim Schalter werden an zwei benachbarte Kontakt je eine zweipolige Stiftleiste gelötet.

### Front

Vorne werden die Lautsprecher mit 8 M5 Zylinderkopfschrauben mit Länge 10 mm und entsprechenden Muttern befestigt.

Für das LCD werden 4 M3 Zylinderkopfschrauben mit Länge 12 mm und entsprechende Muttern benötigt.

Der Verstärker wird mit den beiligenden Utensilien befestigt.

## Zusammenleimen

Man benutze viele viele Schraubzwingen und sanfte Gewalt beim Zusammenstecken.

Der Boden wird nicht verleimt, sondern nur gesteckt. Sollte er nicht halten, muss man sich was schlaues überlegen, dass er es doch tut.

![alt](Doc/Images/rn_image_picker_lib_temp_33dfafee-b81e-48e9-8fad-b0570744117b.jpg)

## Verkabelung

Wenn alles mit rechten Dingen zugegangen ist, sollte jetzt alles mit ordinären Jumperkabeln zu verbinden sein. 

![alt](Doc/Images/IMG_20231115_211402.jpg)

1. Die gecrimpten Buchsen an der USB-C buchse werden auf die Spannungsversorgungspins auf dem HAT gesteckt.
2. Der mit 5V markierte Pin des LCD-Anschlusses wird mit einem Pin am An/Aus-Schalter verbunden.
3. Vom An/Ausschalter werden zwei weitere Jumperkabel (vom anderen Anschluss) an das LCD und den Verstärker geführt.
4. Je zwei Leitungen werden für die Taster benötigt.
5. Den Rest der Verkabelung für LCD und Verstärker, wie im Testaufbau.

Wenn man jetzt das Netzteil einsteckt, sollte nach eineiger Zeit das Radio ertönen.

## Senderliste bearbeiten

Per SSH verbinden:

```
ssh pi@xxx.xxx.xxx.xxx
cd ~/Playlists
nano Playlist.m3u
```

Hier neue Webstreams hinzufügen.

https://streamurl.link/ scheint eine ganz gute Quelle für URLs zu sein.

Speichern mit Strg+O, Enter und Schließen mit Strg+X.

Das WLAN-Radio neu starten. Dabei wird die Playlist neu eingelesen.

```
sudo systemctl restart wlan-radio
```