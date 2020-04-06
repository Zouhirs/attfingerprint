#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code is used to enroll students into the program
'''

# --------------------- Libraries -------------------- #
import time
import json
from os import path, stat
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
- Initialize LCD.
'''
def init():
    global lcd
    global f

    if(path.exists(Info.studentFilePath)==False): raise Exception('File of students doesn\'t exist.')
    f = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    if(f.verifyPassword()==False): raise Exception('Sensor\'s password is incorrect.')

    lcd = lcd_i2c_driver.lcd()

'''
Add student to JSON file:
- Check the file if it exists or is empty and add its structure.
- Load its content
- Construct the student, add it to data, and dump data to the file.
'''
def add_student(id, fname, lname, cin, cne):
    if(path.exists(Info.studentFilePath)==False or stat(Info.studentFilePath).st_size==0):
        with open(Info.studentFilePath, 'w+') as file:
            data = {}
            data['students'] = []
            json.dump(data, file)
        file.close()

    with open(Info.studentFilePath, 'r') as file:
        data = json.load(file)
    file.close()

    student = {'id': id,
               'first_name': fname,
               'last_name': lname,
               'cin': cin,
               'cne': cne}
    data['students'].append(student)

    with open(Info.studentFilePath, 'w') as file:
        json.dump(data, file)
    file.close()

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
First Read of the fingerprint sensor:
- Wait for finger to be detected.
- Convert its image and store it in char buffer 0x01.
- Return position of template
'''
def first_read():
    while(f.readImage()==False): pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    return result[0]

'''
Second Read of the fingerprint sensor:
- Wait for finger to be detected.
- Convert its image and store it in char buffer 0x02.
- Compare the two buffers
'''
def second_read():
    while (f.readImage()==False): pass
    f.convertImage(0x02)
    if (f.compareCharacteristics()==0): return False
    return True

'''
Enroll the student:
- Create corresponding template in the fingerprint sensor.
- Get student's data from input.
- Add student in JSON file with same id as position
'''
def enroll():
    if(f.createTemplate()==True):
        fname = str(input(colored('First Name: ', 'blue')))
        lname = str(input(colored('Last Name: ', 'blue')))
        cin = str(input(colored('CIN: ', 'blue')))
        cne = str(input(colored('CNE: ', 'blue')))
        positionNumber = f.storeTemplate()
        add_student(positionNumber, fname, lname, cin, cne)
        return fname, lname
    return None

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
- Every iteration will try to enroll a student.
- Perform two reads of finger.
- Enroll student.
'''
def main():
    init()
    while(1):
        time.sleep(2)
        lcd_write('Waiting for', 'finger...')
        result = first_read()
        if (result >= 0 ): lcd_write('Template exits', 'at #' + str(result))
        else:
            lcd_write('Remove finger')
            time.sleep(2)
            lcd_write('Waiting for', 'same finger...')
            if (second_read()==False): lcd_write('Fingers do', 'not match')
            else:
                lcd_write('Please enter', 'your info')
                fname, lname = enroll()
                if(fname is not None and lname is not None):
                    lcd_write(fname + " " + lname, 'enrolled')
                    print(colored(fname + " " + lname, 'yellow') + " enrolled successfully.\n\n")
                else:
                    lcd_write('Error adding', 'template')
                    print('Error adding template.\n\n')

# --------------------------------------------------------- #

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: cleanup()
    except Exception as e:
        print('Exception: ' + str(e))
        cleanup()
