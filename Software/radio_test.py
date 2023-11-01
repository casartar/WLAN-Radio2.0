import RPi.GPIO as GPIO
from mpd import MPDClient
import time

# Initialisiere GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO-Pin für vorwärts-Taster
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO-Pin für rückwärts-Taster

# Verbindung zum MPD-Server herstellen
client = MPDClient()
client.connect("localhost", 6600)

def next(channel):
    GPIO.remove_event_detect(4)
    status = client.status()
    current_song = int(status["song"])
    total_songs = int(status["playlistlength"])

    if current_song == total_songs - 1:
        print("Next - Jump to first")
        client.play(0)
    else:
        print("Next")
        client.next()
    print(client.status())
    print(client.currentsong())

    GPIO.add_event_detect(4, GPIO.FALLING, callback=next, bouncetime=300)

def previous(channel):
    GPIO.remove_event_detect(17)
    status = client.status()
    current_song = int(status["song"])
    total_songs = int(status["playlistlength"])
    
    if current_song == 0:
        print("Previous - Jump to last")
        client.play(total_songs - 1)
    else:
        print("Previous")
        client.previous()
    print(client.status())
    print(client.currentsong())

    GPIO.add_event_detect(17, GPIO.FALLING, callback=previous, bouncetime=300)

# Event Handler für Tasten
GPIO.add_event_detect(4, GPIO.FALLING, callback=next, bouncetime=300)
GPIO.add_event_detect(17, GPIO.FALLING, callback=previous, bouncetime=300)
client.clear()
client.load("playlist")
client.play(0)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()