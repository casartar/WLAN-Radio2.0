import time
from mpd import MPDClient

# MPD
client = MPDClient()
client.timeout = 10
client.idletimeout = None
client.connect("localhost", 6600)
print(client.mpd_version)

if __name__ == '__main__':
    client.clear()
    client.load("Playlist")
    client.play(0)

    while True:
        client.next()
        time.sleep(5)
