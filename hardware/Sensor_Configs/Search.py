#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code is used to search corresponding student from fingerprint
'''

# --------------------- Libraries -------------------- #
import json
import time
from os import path
from termcolor import colored
from pyfingerprint.pyfingerprint import PyFingerprint
import lcd_i2c_driver
import Info
# ---------------------------------------------------- #

# --------------------- Functions ------------------------- #

'''
Initializing:
- Check students file.
- Connect to the fingerprint sensor and verify its password.
- Print header.
'''
def init():
    global f
    global lcd

    if(path.exists(Info.studentFilePath)==False): raise Exception('File of students doesn\'t exist.')
    f = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    if(f.verifyPassword()==False): raise Exception('Sensor\'s password is incorrect.')
    lcd = lcd_i2c_driver.lcd()

'''
Get Students data from JSON file.
'''
def load_data():
    with open(Info.studentFilePath, 'r') as file:
        data = json.load(file)
    file.close()
    return data['students']

'''
Search for the template the fingerprint sensor:
- Wait for finger to be detected.
- Convert its image and store it in char buffer 0x01.
- Return position of template
'''
def search_template():
    while(f.readImage()==False): pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    return result[0]

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
Cleanup at exit:
- add a line for better apperance in terminal.
- clear LCD screen.
- exit the program.
'''
def cleanup():
    print()
    lcd.lcd_clear()
    exit()

'''
Main Program:
'''
def main():
    init()
    students = load_data()
    while(1):
        time.sleep(2)
        match_found = False
        print(colored('\nWaiting for finger... ', 'blue'))
        lcd_write('Waiting for', 'finger')
        pos = search_template()
        for student in students:
            if student['id'] == pos:
                match_found = True
                print('Student found: ' + colored(student['first_name'] + " " + student['last_name'], 'yellow') + ' at position ' + colored('#' + str(pos), 'red'))
                lcd_write(student['first_name'], student['last_name'])
        if(match_found == False):
            print('No match found.')
            lcd_write('No match', 'found')

# --------------------------------------------------------- #

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: cleanup()
    except Exception as e:
        print('Exception: ' + str(e))
        cleanup()
