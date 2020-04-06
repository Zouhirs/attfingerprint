#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code is the main program
'''

# --------------------- Libraries -------------------- #
import json
import time
import threading
from os import path
from pyfingerprint.pyfingerprint import PyFingerprint
import lcd_i2c_driver
import RPi.GPIO as GPIO
import Info
import Server
# ---------------------------------------------------- #

# ------- Pins ------ #
gpio_RED = 24
gpio_GREEN = 23
gpio_BUZZER = 18
# ------------------ #

# --------------------- Functions ------------------------- #

'''
Initializing:
- Setup GPIOs.
- Connect to the server's database.
- Initialize fingerprint sensor and LCD.
'''
def init():
    global lcd
    global f

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_RED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(gpio_GREEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(gpio_BUZZER, GPIO.OUT, initial=GPIO.LOW)

    Server.connect()
    if(Server.getCurrentModule()==None):
        Server.close()
        exit(0)
    f = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    lcd = lcd_i2c_driver.lcd()
    beep(2,0.05)

'''
Beeps the buzzer:
'''
def beep(count, period):
    for i in range(count):
        GPIO.output(gpio_BUZZER, GPIO.HIGH)
        time.sleep(period)
        GPIO.output(gpio_BUZZER, GPIO.LOW)
        time.sleep(period)

'''
Toggle LEDs based on the mode:
'''
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

'''
Write to lCD:
- Clear it.
- Display first argument in first line.
- Display second argument in second line.
'''
def lcd_write(firstline, secondline=''):
    lcd.lcd_clear()
    lcd.lcd_display_string(firstline, 1)
    lcd.lcd_display_string(secondline, 2)

'''
Get Students data from JSON file.
'''
def load_data():
    with open(Info.studentFilePath, 'r') as file:
        data = json.load(file)
    file.close()
    return data['students']

'''
Search for the student in data based on given id.
'''
def getStudentFromID(id, data):
    for student in data:
        if(student['id'] == id) : return student
    return None

'''
Search for the template the fingerprint sensor, respecting provided timeout:
- Wait for finger to be detected.
- Convert its image and store it in char buffer 0x01.
- Return position of template
'''
def search_template(timeout):
    while(f.readImage()==False):
        leds(0)
        if (time.time() > timeout) : return None
    f.convertImage(0x01)
    result = f.searchTemplate()
    return result[0]

'''
Cleanup at exit:
- Put GPIOs output to LOW and put them all as input.
- add a line for better apperance in terminal.
- clear LCD screen.
- Close connection to server.
- exit the program.
'''
def cleanup():
    GPIO.output(gpio_RED, GPIO.LOW)
    GPIO.output(gpio_GREEN, GPIO.LOW)
    GPIO.output(gpio_BUZZER, GPIO.LOW)
    GPIO.cleanup()
    print()
    lcd.lcd_clear()
    Server.close()
    exit()

'''
Main Program:
- Provide the maximum time for registring presence.
- Provide an array of already registred students in current module.
- Load students data from JSON file.
- Wait for fingerprint and search for the corresponding student.
- If the student is known, register him in database.
'''
def main():
    init()
    start = time.time() # get current time
    PERIOD_OF_TIME = 60*30 # timeout period
    timeout = False
    presentStudentsIds = []
    data = load_data()
    while(1):
        lcd_write('Waiting for', 'finger | ' + Server.getCurrentModule()[0])
        result = search_template(start + PERIOD_OF_TIME)

        if result is None : raise ValueError('Timeout')

        elif (result == -1):
            threading.Thread(target=beep, args=(1,0.2)).start()
            leds(2)
            lcd_write('No match', 'Please try again')

        else:
            threading.Thread(target=beep, args=(2,0.05)).start()
            leds(1)
            student = getStudentFromID(result, data)
            if student['id'] not in presentStudentsIds:
                lcd_write(student['first_name'], student['last_name'])
                Server.setToPresent(str(student['id']))
                presentStudentsIds.append(student['id'])
            else:
                lcd_write('Already', 'Registred')
        time.sleep(2)
    cleanup()

# --------------------------------------------------------- #

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, ValueError): cleanup()
    except Exception as e:
        print("Exception : " + str(e))
        cleanup()
