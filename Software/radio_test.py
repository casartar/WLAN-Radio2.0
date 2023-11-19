import time
import datetime
import RPi.GPIO as GPIO
from mpd import MPDClient
from RPLCD.i2c import CharLCD
import socket

# GPIO
nextButton = 4
prevButton = 17

nextButtonRequest = False
prevButtonRequest = False

# MPD
client = MPDClient()

# LCD
LCD_LEN = 16
LCD_MAX_WAIT = 2
backlightOnRequest = True

currentSong = ""
currentName = ""

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

def next(channel):
    GPIO.remove_event_detect(nextButton)
    global backlightOnRequest
    backlightOnRequest = True
    global nextButtonRequest
    nextButtonRequest = True
    time.sleep(0.3)
    GPIO.add_event_detect(nextButton, GPIO.FALLING, callback=next, bouncetime=300)

def previous(channel):
    GPIO.remove_event_detect(prevButton)
    global backlightOnRequest
    backlightOnRequest = True
    global prevButtonRequest
    prevButtonRequest = True
    time.sleep(0.3)
    GPIO.add_event_detect(prevButton, GPIO.FALLING, callback=previous, bouncetime=300)

def LcdScrolling(String):
    current_time = datetime.datetime.now()
    if String != LcdScrolling.workingstring:
        LcdScrolling.index = 0
        LcdScrolling.wait = 0
        LcdScrolling.workingstring = String
        print(String)
    if current_time >= LcdScrolling.last_time + datetime.timedelta(milliseconds=500):
        LcdScrolling.last_time = current_time

        try:
            lcd.cursor_pos = (0, 0)
            lcd.write_string(LcdScrolling.workingstring[LcdScrolling.index:LcdScrolling.index+LCD_LEN])
        except:
            print("lcd.write_string failed")
        #print(LcdScrolling.workingstring[LcdScrolling.index:LcdScrolling.index+LCD_LEN])
        if LcdScrolling.wait < LCD_MAX_WAIT:
            LcdScrolling.wait = LcdScrolling.wait + 1
        elif LcdScrolling.index >= len(LcdScrolling.workingstring)-LCD_LEN:
            LcdScrolling.index = 0
            LcdScrolling.wait = 0
        else:
            LcdScrolling.index = LcdScrolling.index + 1

def UpdateLcd():
    if datetime.datetime.now() >= UpdateLcd.update_time:
        UpdateLcd.update_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
        global currentSong
        try:
            currentSong = client.currentsong()["title"]
            #print("title: " + str(currentSong))
        except:
            currentSong = "No title available"
            #print("NO title")
        global currentName
        try:
            current_name = str(client.currentsong()["name"])
        except:
            current_name = "No name"

        if currentName != current_name:
            currentName = current_name
            lcd.cursor_pos = (1, 0)
            lcd.write_string(currentName[0:LCD_LEN].ljust(LCD_LEN))
            print("name: " + currentName)



def BacklightHandler():
    global backlightOnRequest
    if backlightOnRequest:
        BacklightHandler.turn_off_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
        lcd._set_backlight_enabled(True)
        backlightOnRequest = False
        BacklightHandler.backlightOnFlag = True
        print("Backlight on")
    if datetime.datetime.now() >= BacklightHandler.turn_off_time and BacklightHandler.backlightOnFlag:
        BacklightHandler.backlightOnFlag = False
        lcd._set_backlight_enabled(False)
        print("Backlight off")

def GpioHandler():
    global nextButtonRequest
    global prevButtonRequest

    if nextButtonRequest:
        nextButtonRequest = False

        status = client.status()
        current_song = int(status["song"])
        total_songs = int(status["playlistlength"])

        if current_song == total_songs - 1:
            print("Next - Jump to first")
            client.play(0)
        else:
            print("Next")
            client.next()

        #print(client.status())
        #print(client.currentsong())

    elif prevButtonRequest:
        prevButtonRequest = False

        status = client.status()
        current_song = int(status["song"])
        total_songs = int(status["playlistlength"])
        
        if current_song == 0:
            print("Previous - Jump to last")
            client.play(total_songs - 1)
        else:
            print("Previous")
            client.previous()

        #print(client.status())
        #print(client.currentsong())


if __name__ == '__main__':
    client.connect("localhost", 6600)

    # GPIO    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(nextButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(prevButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(nextButton, GPIO.FALLING, callback=next, bouncetime=300)
    GPIO.add_event_detect(prevButton, GPIO.FALLING, callback=previous, bouncetime=300)
    
    # MPD
    client.clear()
    client.load("Playlist")
    client.play(0)

    try:
        LcdScrolling.workingstring = 0
        LcdScrolling.last_time = datetime.datetime.now()
        LcdScrolling.index = 0
        LcdScrolling.wait = 0
        BacklightHandler.turn_off_time = datetime.datetime.now()
        BacklightHandler.backlightOnFlag = False
        UpdateLcd.update_time = datetime.datetime.now()
        while True:
            LcdScrolling(currentSong)
            #BacklightHandler()
            GpioHandler()
            UpdateLcd()

    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()