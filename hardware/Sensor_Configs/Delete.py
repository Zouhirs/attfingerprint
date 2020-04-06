#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code is used to delete a students or all.
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
'''
def init():
    global f

    if(path.exists(Info.studentFilePath)==False): raise Exception('File of students doesn\'t exist.')
    f = PyFingerprint(Info.portPath, 9600*6, 0xFFFFFFFF, 0x00000000)
    if(f.verifyPassword()==False): raise Exception('Sensor\'s password is incorrect.')

'''
Get Students data from JSON file.
'''
def load_data():
    with open(Info.studentFilePath, 'r') as file:
        data = json.load(file)
    file.close()
    return data

'''
Delete all data:
- Confirm deletion.
- Load data, delete students, re-write data in file.
- Clear sensor's database.
'''
def clear_all():
    resp = input(colored('[Warning]', 'red') + ': All data will be deleted. Continue? [y|n]: ')
    if(resp == 'y'):
        data = load_data()
        data['students'] = []
        with open(Info.studentFilePath, 'w') as file:
            json.dump(data, file)
        file.close();
        if (f.clearDatabase() == True):
            print('All Templates deleted')

'''
Delete a student:
- Load data.
- Search for student with given id.
- Confirm deletion.
- Remove the student from data and re-write it in file.
- Delete template from the sensor
'''
def delete_student(id):
    data = load_data()
    for student in data['students']:
        if student['id'] == id :
            first_name = student['first_name']
            last_name = student['last_name']
            resp = input(colored('[Warning]', 'red') + " " + first_name + " " + last_name + " will be deleted. Continue? [y|n]: ")
            if(resp == 'y'):
                data['students'].remove(student)
                if ( f.deleteTemplate(id) == True ):
                    print('Template deleted.')
                    with open(Info.studentFilePath, 'w') as file:
                        json.dump(data, file)
                        file.close()

'''
Cleanup at exit:
- add a line for better apperance in terminal.
- exit the program.
'''
def cleanup():
    print()
    exit()

'''
Main Program:
'''
def main():
    init()
    id = int(input('Please enter the template position you want to delete ' + colored('(-1 to delete all)', 'red') + ': '))
    if(id==-1): clear_all()
    else: delete_student(id)

# --------------------------------------------------------- #

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: cleanup()
    except Exception as e:
        print('Exception: ' + str(e))
        cleanup()
