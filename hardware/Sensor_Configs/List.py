#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code is used to list the students enrolled with their infos.
'''

# --------------------- Libraries -------------------- #
import json
from os import path
from termcolor import colored
from pyfingerprint.pyfingerprint import PyFingerprint
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

    if(path.exists(Info.studentFilePath)==False): raise Exception('File of students doesn\'t exist.')
    f = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    if(f.verifyPassword()==False): raise Exception('Sensor\'s password is incorrect.')
    print('\n'+colored('ID/Position'.ljust(30),'red')+colored('First Name'.ljust(30),'red')+colored('Last Name'.ljust(30),'red')+colored('CIN'.ljust(30),'red')+colored('CNE','red'))

'''
Get Students data from JSON file.
'''
def load_data():
    with open(Info.studentFilePath, 'r') as file:
        data = json.load(file)
    file.close()
    return data['students']

'''
Print students data
'''
def print_students(data):
    for i in range(0, len(data)):

        id = str(data[i]['id'])
        first_name = str(data[i]['first_name'])
        last_name = str(data[i]['last_name'])
        cin = str(data[i]['cin'])
        cne = str(data[i]['cne'])

        print(id.ljust(30)+first_name.ljust(30)+last_name.ljust(30)+cin.ljust(30)+cne)

'''
Cleanup at exit:
- add a line for better apperance in terminal.
- exit the program.
'''
def cleanup():
    print()
    exit()

'''
Main Program
'''
def main():
    init()
    print_students(load_data())
    print('\nSensor used templates : ' + colored(str(f.getTemplateCount()), 'yellow'))

# --------------------------------------------------------- #

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: cleanup()
    except Exception as e:
        print('Exception: ' + str(e))
        cleanup()
