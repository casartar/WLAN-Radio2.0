from threading import Thread, Event
import time
import RPi.GPIO as GPIO
from mpd import MPDClient
from RPLCD.i2c import CharLCD
import Encoder

# Threading
lcd_event = Event()
backlight_on_event = Event()
backlight_timeout_event = Event()
backlight_off_event = Event()

# GPIO
nextButton = 4
prevButton = 17
playButton = 25
encoder1 = 23
encoder2 = 24

# MPD
client = MPDClient()
client.timeout = 10
client.idletimeout = None
client.connect("localhost", 6600)
print(client.mpd_version)

# LCD
lcd_string1 = ""
lcd_string2 = ""
LCD_LEN = 16
LCD_MAX_WAIT = 5

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# Encoder
enc = Encoder.Encoder(encoder1, encoder2)
old_encoder_value = 0


def PollGpio():

    while True:
        global old_encoder_value
        #encoder_value = enc.read()
        if GPIO.input(nextButton) == False:
            print("Next")
            try:
                backlight_on_event.set()
                client.next()
                client.play()
            except:
                print("Failed")
        elif GPIO.input(prevButton) == False:
            print("Prev")
            try:
                backlight_on_event.set()
                client.previous()
                client.play()
            except:
                print("Failed")
        elif GPIO.input(playButton) == False:
            print("Toggle")
            backlight_on_event.set()
            client.pause()
        #elif encoder_value != old_encoder_value:
        #    print("Volume Change: " + str(encoder_value - old_encoder_value))
        #    client.volume(encoder_value - old_encoder_value)
        #    old_encoder_value = encoder_value
        time.sleep(0.15)


def DataUpdate():
    current_song_title = ""
    current_name = ""
    while True:
        try:
            current_song_title = client.currentsong()["title"]
            print("title: " + str(current_song_title))
        except:
            print("NO title")
        try:
            current_name = str(client.currentsong()["name"])
            print("name: " + current_name)
        except:
            print("NO name")
        print("")
        global lcd_string1
        global lcd_string2
        if current_song_title != lcd_string1:
            lcd_string1 = current_song_title
            lcd_event.set()
        if current_name != lcd_string2:
            lcd_string2 = current_name
        time.sleep(10)


def LcdThread():
    workingstring = ""
    index = 0
    wait = 0
    while True:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(workingstring[index:index+LCD_LEN])
        print(workingstring[index:index+LCD_LEN])
        if lcd_event.is_set():
            lcd_event.clear()
            index = 0
            wait = 0
            workingstring = lcd_string1
        if wait < LCD_MAX_WAIT:
            wait = wait + 1
        elif index >= len(workingstring)-LCD_LEN:
            index = 0
            wait = 0
        else:
            index = index + 1
        if backlight_on_event.is_set():
            backlight_on_event.clear()
            lcd._set_backlight_enabled(True)
            backlight_timeout_event.set()
        if backlight_off_event.is_set():
            backlight_off_event.clear()
            lcd._set_backlight_enabled(False)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(lcd_string2[0:LCD_LEN].ljust(LCD_LEN))

        time.sleep(1)


def BacklightThread():
    while True:
        if backlight_timeout_event.is_set():
            backlight_timeout_event.clear()
            time.sleep(10)
            backlight_off_event.set()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(nextButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(prevButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(playButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    lcd.write_string('WLAN Radio')
    lcd.cursor_pos = (1, 0)
    lcd.write_string("1234567890abcdef")

    client.clear()
    client.load("playlist")
    client.play(0)

    polling_thread = Thread(target=PollGpio)
    lcd_thread = Thread(target=LcdThread)
    update_thread = Thread(target=DataUpdate)
    backlight_thread = Thread(target=BacklightThread)
    polling_thread.start()
    lcd_thread.start()
    update_thread.start()
    backlight_thread.start()

    backlight_on_event.set() 
