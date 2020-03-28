'''
This code contains the methods used in the main program
'''

# --------------------- Libraries -------------------- #
import time
from os import path
from pyfingerprint.pyfingerprint import PyFingerprint
import lcd_i2c_driver as lcd_i2c
import RPi.GPIO as GPIO
import Server
import Info
# ---------------------------------------------------- #

# ------- Pins ------ #
gpio_RED = 24
gpio_GREEN = 23
gpio_BUZZER = 18
# ------------------ #

# ------------ Setup ---------- #
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(gpio_RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(gpio_GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(gpio_BUZZER, GPIO.OUT, initial=GPIO.LOW)
# ----------------------------- #

#------------------ Functions ---------------- #
def init():
    global lcd
    global fingerSensor
    Server.connect()
    if(Server.getCurrentModule()==None):
        Server.close()
        exit(0)
    fingerSensor = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    time.sleep(1)
    lcd = lcd_i2c.lcd()
    beep(2,0.05)

def beep(count, period):
    for i in range(count):
        GPIO.output(gpio_BUZZER, GPIO.HIGH)
        time.sleep(period)
        GPIO.output(gpio_BUZZER, GPIO.LOW)
        time.sleep(period)

def leds(mode):
    if(mode==0): # waiting
        GPIO.output(gpio_GREEN, GPIO.HIGH)
        GPIO.output(gpio_RED, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(gpio_RED, GPIO.LOW)
        GPIO.output(gpio_GREEN, GPIO.LOW)
    elif(mode==1): # template found
        GPIO.output(gpio_GREEN, GPIO.HIGH)
        GPIO.output(gpio_RED, GPIO.LOW)
    elif(mode==2): # template not found
        GPIO.output(gpio_GREEN, GPIO.LOW)
        GPIO.output(gpio_RED, GPIO.HIGH)
    else: raise ValueError("Leds mode not supported.")

def lcd_write(firstline, secondline=''):
    lcd.lcd_clear()
    lcd.lcd_display_string(firstline, 1)
    lcd.lcd_display_string(secondline, 2)

def searchFingerprint():
    # convert image to characteristics
    # and store it in char buffer 0x01
    fingerSensor.convertImage(0x01)
    # search for the template in
    # sensor's memory
    result = fingerSensor.searchTemplate()
    # get the result
    positionNumber = result[0]
    # if it exists
    if(positionNumber == -1): return None
    # if it does not exist
    else: return positionNumber

def getStudentFromID(id, data):
    for student in data['students']:
        if(student['id'] == id) : return student
    return None

def cleanup():
    GPIO.output(gpio_RED, GPIO.LOW)
    GPIO.output(gpio_GREEN, GPIO.LOW)
    GPIO.output(gpio_BUZZER, GPIO.LOW)
    lcd.lcd_clear()
    GPIO.cleanup()
    Server.close()
# ------------------------------------------------ #
