#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from mysql.connector import Error
from click import echo, style, clear

def enroll(db, cursor, sensor, track, year, number):
    '''
    Enroll Student Main Function:
    - Read fingerprint with double checking.
    - Get student info: first and last name.
    - Store fingerprint in the sensor and get position of it in the memory.
    - Add student to the server and use position as id.
    '''

    clear()
    for student in range(0, number):
        echo(style('-------------- Student {} out of {} --------------:\n'.format(student+1, number), fg='black', bold=True))
        read = 1
        while(read):
            read = read_fingerprint(sensor, 0x01)
            time.sleep(2)
            if not read : read = read_fingerprint(sensor, 0x02)

        echo(style(' [\u2713] ', fg='green', bold=True) + style('Success.\n', bold=True))

        firstname, lastname = None, None
        while (firstname is None and lastname is None):
            firstname, lastname = get_info()

        pos = store_fingerprint(sensor)
        if pos != -1: add_to_server(db, cursor, pos, firstname, lastname, track, year)

        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} {} added successfully.\n'.format(firstname, lastname), bold=True))

def read_fingerprint(sensor, buffer):
    '''
    Read Fingerprint:
    - Wait for fingerprint.
    - Convert image and store in buffer 0x01.
    - Check if it already exists.
    - Wait for fingerprint.
    - Convert image and store in buffer 0x02.
    - Check if the two two buffers are similar.
    '''

    echo(style(' [?] ', fg='yellow', bold=True) + style('Please place your finger.', bold=True))
    while(not sensor.readImage()): pass
    echo(style(' [!] ', fg='blue', bold=True) + style('Finger detected, please hold.', bold=True))

    sensor.convertImage(buffer)
    if(buffer == 0x01):
        result = sensor.searchTemplate()[0]
        if result >= 0:
            echo(style(' [x] ', fg='red', bold=True) + style('Fingerprint already exists at position #{}.\n'.format(result), bold=True))
            time.sleep(2)
            return 1
        else: return 0

    elif(buffer == 0x02):
        result = sensor.compareCharacteristics()
        if result == False:
            echo(style(' [x] ', fg='red', bold=True) + style('Fingerprints don\'t match.\n', bold=True))
            time.sleep(2)
            return 1
        else: return 0

def get_info():
    '''
    Get Student Info:
    - First name.
    - Last name.
    - Check provided data.
    '''

    firstname = str(input(style(' [?] ', fg='yellow', bold=True) + style('Please provid first name: ', bold=True)))
    lastname = str(input(style(' [?] ', fg='yellow', bold=True) + style('Please provid last name: ', bold=True)))
    if(firstname.replace(' ','').isalpha() == False or firstname == "" or lastname.replace(' ','').isalpha() == False or lastname == ""):
        echo(style(' [x] ', fg='red', bold=True) + style('Name is not supported.\n', bold=True))
        return None, None
    return firstname, lastname

def store_fingerprint(sensor):
    '''
    Store Fingerprint in the Sensor:
    - Create template from the two buffers.
    - Store it in memory and get the position.
    '''

    res = sensor.createTemplate()
    if res == True:
        pos = sensor.storeTemplate()
        return pos
    else:
        echo(style(' [x] ', fg='red', bold=True) + style('Error storing template.\n', bold=True))
        return -1

def add_to_server(db, cursor, id, fname, lname, track, year):
    '''
    Add Student to File.
    - Load data already stored in file.
    - Append new student to data.
    - Store it in the file.
    '''

    query = "INSERT INTO {}_{}_Students (`id`, `first_name`, `last_name`) VALUES (%s, %s, %s)".format(track, year)

    try:
        cursor.execute(query, (id, fname, lname))
        db.commit()
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
