#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from click import echo, style, clear
from mysql.connector import Error

def search(db, cursor, sensor, track, year):
    '''
    Search in Data for Fingerprint:
    - Read fingerprint.
    - Load data if found.
    - Return the full name of student.
    '''

    pos = read_fingerprint(sensor)
    if pos >= 0:
        query = "SELECT * FROM {}_{}_Students WHERE `id`={}".format(track, year, pos)

        try:
            cursor.execute(query)
            student = cursor.fetchall()
            if student:
                echo(style(' [\u2713] ', fg='green', bold=True) + style('Match found: ', bold=True) + style('{} {}.'.format(student[0]['first_name'], student[0]['last_name']), fg='green', bold=True))
            else:
                echo(style(' [x] ', fg='red', bold=True) + style('Database and sensor are out of sync.', bold=True))
        except Error as err:
            echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
    else:
        echo(style(' [x] ', fg='red', bold=True) + style('No match found or sensor\'s database is empty.', bold=True))


def read_fingerprint(sensor):
    '''
    Read Fingerprint:
    - Wait for fingerprint.
    - Convert image and store in buffer 0x01.
    - Check if it exists and return position.
    '''

    echo(style(' [?] ', fg='yellow', bold=True) + style('Please place your finger.', bold=True))
    while(not sensor.readImage()): pass
    echo(style(' [!] ', fg='blue', bold=True) + style('Finger detected, please hold.', bold=True))

    sensor.convertImage(0x01)
    result = sensor.searchTemplate()
    return result[0]
